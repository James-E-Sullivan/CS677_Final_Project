import requests, io, json, codecs, copy, time
import pandas as pd
import data_collection.manifest_hash_functions as manifest


# dictionary to hold extra headers
HEADERS = {"X-API-Key": '3ac88e4a357e47089618de29c972fbab'}

default_url = "https://bungie.net/Platform"

# build dict of hash_id values mapped to json dictionary descriptions
description_dicts = manifest.build_item_dict(manifest.hashes_trunc)
item_dict = description_dicts['DestinyInventoryItemDefinition']


class DestinyAccount:
    """
    Class used to hold/return Destiny 2 account information
    """

    def __init__(self, name, platform='-1'):
        self._name = name
        self._platform = platform
        search_player_path = "/Destiny2/SearchDestinyPlayer/" + str(platform) +\
                             "/" + name + "/"
        req = requests.get(default_url + search_player_path, headers=HEADERS)
        self._request_json = req.json()
        self._user_info = self._request_json['Response'][0]
        self._membership_type = self._user_info['membershipType']
        self._membership_id = self._user_info['membershipId']

    def get_character_ids(self):
        """
        obtain character id hash values for account
        :return: list of character id hash values
        """
        character_path = "/Destiny2/" + str(self._user_info['membershipType']) +\
                       "/Profile/" + self._user_info['membershipId'] +\
                       "/?components=100"

        req = requests.get(default_url + character_path, headers=HEADERS)
        return req.json()['Response']['profile']['data']['characterIds']

    @property
    def membership_type(self):
        return self._membership_type

    @property
    def membership_id(self):
        return self._membership_id

    @property
    def name(self):
        return self._name


def get_comp_match_ids(account, mode=69, matches=100):
    """
    Obtain instanceId values of activity data for each character.
    Mode set to 69, which narrows search to competitive crucible matches.
    Activity type can be changed if user has dict of mode values.
    :param account: DestinyAccount object
    :param mode: Activity type enum value
    :param matches: Maximum # of matches to search (per character)
    :return: All instanceId values returned from search
    """

    # id hashes for each character associated with account
    character_ids = account.get_character_ids()

    instance_id_values = []  # used to store activity instanceId values

    for character in character_ids:

        activity_path = "/Destiny2/" + str(account.membership_type) + \
                        "/Account/" + account.membership_id + \
                        "/Character/" + character +\
                        "/Stats/Activities/?count=" + str(matches) +\
                        "&mode=" + str(mode)

        req = requests.get(default_url + activity_path, headers=HEADERS)
        character_activity_json = req.json()

        if not character_activity_json['Response']:
            # no character activity data - dict is empty
            continue
        else:
            character_activities = character_activity_json['Response']['activities']

            for activity in character_activities:
                instance_id_values.append(activity['activityDetails']['instanceId'])

    return instance_id_values


def get_destiny_manifest():

    """
    Obtain Destiny 2 manifest json. This will give the user
    endpoints from which they can download manifest sqlite3 db's
    in their preferred language
    :return: manifest json
    """

    manifest_path = "/Destiny2/Manifest/"
    req = requests.get(default_url + manifest_path, headers=HEADERS)
    return req.json()


def get_game_stats(game_id, account):
    """game_id from instance_id_values list"""

    # Destiny2.GetPostGameCarnageReport
    pgcr_path = "/Destiny2/Stats/PostGameCarnageReport/" + game_id
    req = requests.get(default_url + pgcr_path, headers=HEADERS)

    pgcr_info = req.json()

    pgcr_entries = pgcr_info['Response']['entries']

    # iterate through players listed in PGCR
    for player in pgcr_entries:

        player_info = player['player']['destinyUserInfo']

        # only get player info for specified account
        if player_info['membershipId'] == account.membership_id:

            stats = player['values']

            try:
                weapons_list = player['extended']['weapons']
            except KeyError as e:
                # no weapons in player PGCR extended data
                weapons_list = []

            # compile player info into dictionary
            player_dict = {'display_name': player_info['displayName'],
                           'membership_id': player_info['membershipId'],
                           'class': player['player']['characterClass'],
                           'score': stats['score']['basic']['value'],
                           'kills': stats['kills']['basic']['value'],
                           'deaths': stats['deaths']['basic']['value'],
                           'assists': stats['assists']['basic']['value'],
                           'avg_score_per_life': stats[
                               'averageScorePerLife']['basic']['value'],
                           'opponents_defeated': stats[
                               'opponentsDefeated']['basic']['value'],
                           'efficiency': stats['efficiency']['basic']['value'],
                           'kdr': stats['killsDeathsRatio']['basic']['value'],
                           'kda': stats['killsDeathsAssists']['basic']['value'],
                           'standing': stats['standing']['basic']['value'],
                           'team_score': stats['teamScore']['basic']['value']}

            if weapons_list:

                top_weapon = weapons_list[0]

                reference_id = top_weapon['referenceId']
                weapon_kills = top_weapon['values'][
                    'uniqueWeaponKills']['basic']['value']

                # get weapon (name,type) tuple from manifest
                w_name_type = manifest.name_type_by_hash(
                    reference_id, item_dict)
                weapon_name = w_name_type[0]
                weapon_type = w_name_type[1]

                name_col = 'weapon_name'
                type_col = 'weapon_type'
                kills_col = 'weapon_kills'

                player_dict[name_col] = weapon_name
                player_dict[type_col] = weapon_type
                player_dict[kills_col] = weapon_kills

            game_df = pd.DataFrame.from_dict(player_dict, orient='index')
            return game_df.T  # return transposed game stats df

    print('User not found in PGCR')


def get_comp_stat_df(account):
    """
    Compile a pandas DataFrame of match data for one account
    (multiple competitive matches)
    :param account: DestinyAccount object
    :return: Compiled account match DataFrame
    """
    match_ids = get_comp_match_ids(account)

    comp_stats_df = pd.DataFrame()

    print('\nCompiling match data. for ' + account.name +
          '. This may take a few minutes...')

    for match in match_ids:

        # obtain df of game statistics
        match_stats = get_game_stats(match, account)

        # append each match to df of all match stats
        comp_stats_df = comp_stats_df.append(match_stats, ignore_index=True,
                                             sort=False)

    print('Match data compilation for ' + account.name + ' is complete.\n')

    return comp_stats_df


if __name__ == '__main__':

    pd.set_option('display.max_rows', 100)
    pd.set_option('display.width', 500)
    pd.set_option('display.max_columns', 50)

    account_names = ['IX Fall0ut XI',
                     'PureChilly',
                     'Seamusin',
                     'NeutralDefault']

    my_account = DestinyAccount('Seamusin')

    print('Competitive Matches Returned with Request to Bungie API: ',
          len(get_comp_match_ids(my_account)))

    print(get_comp_stat_df(my_account))
