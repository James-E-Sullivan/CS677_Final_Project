import requests
import io
import json
import codecs
import pandas as pd
import copy

# dictionary to hold extra headers
HEADERS = {"X-API-Key": '3ac88e4a357e47089618de29c972fbab'}

default_url = "https://bungie.net/Platform"

'''
r = requests.get("https://bungie.net/Platform/Destiny2/SearchDestinyPlayer/-1/Seamusin/", headers=HEADERS)
#r = requests.get()

user_request = r.json()


def get_response(request_json):
    """
    Get 'Response' info from request
    :param request_json: response from requests.get().json()
    :return: dictionary containing response info
    """
    return user_request['Response'][0]


#user_info = user_request['Response'][0]  # dictionary of user info
user_info = get_response(user_request)
print(user_request)

#historical_stats_url = default_url + "/Destiny2/" + user_info['membershipType'] + "/Account/" + user_info['membershipId'] + "/Character"

#r = requests.get(default_url + "/Destiny2/2/Profile/" + user_info['membershipId'] + "/?components=100", headers=HEADERS)

# example of working request using Bungie API documentation
r = requests.get(default_url + "/User/GetMembershipsById/" + user_info['membershipId'] + "/" + str(user_info['membershipType']) + "/", headers=HEADERS)

membership_info = get_response(r.json())


# get profile
# need to figure out why the components=100 part is necessary
profile_path = "/Destiny2/" + str(user_info['membershipType']) + "/Profile/" + user_info['membershipId'] + "/?components=100"


r = requests.get(default_url + profile_path, headers=HEADERS)
profile_request = r.json()

# obtain character id values (up to 3)
character_ids = profile_request['Response']['profile']['data']['characterIds']


'''

'''
# get historic stats for account
historic_stats_path = "/Destiny2/" + str(user_info['membershipType']) + "/Account/" + user_info['membershipId'] + "/Stats"
r = requests.get(default_url + historic_stats_path, headers=HEADERS)

historic_stats_info = r.json()

print(historic_stats_info['Response']['mergedAllCharacters']['results']['allPvP'].keys())
'''


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


def get_comp_match_ids(account, matches=100):

    character_ids = account.get_character_ids()

    # Destiny2.GetActivityHistory (for first character, comp only (mode=69))
    activity_history_path = "/Destiny2/" + str(account.membership_type) +\
                            "/Account/" + account.membership_id +\
                            "/Character/" + character_ids[0] +\
                            "/Stats/Activities/?mode=69"

    req = requests.get(default_url + activity_history_path, headers=HEADERS)

    activity_history_info = req.json()

    #print(activity_history_info['Response']['activities'])

    instance_id_values = []
    match_count = 0
    for i in activity_history_info['Response']['activities']:
        if match_count > matches:
            return instance_id_values  # stop at desired match count
        else:
            instance_id_values.append(i['activityDetails']['instanceId'])

        match_count += 1

    return instance_id_values


def get_destiny_manifest():

    # /common/destiny2_content/sqlite/en/world_sql_content_6a74c8e2272ec3f899cba933f5bcc04c.content

    manifest_path = "/Destiny2/Manifest/"
    req = requests.get(default_url + manifest_path, headers=HEADERS)
    return req.json()

'''
def get_weapon_by_id(reference_id, account):
    id_string = str(reference_id)
    weapon_path = "/Destiny2/" + str(account.membership_type) + "/Profile/" + account.name + "/Item/" + id_string + "/"
    req = requests.get(default_url + weapon_path, headers=HEADERS)
    return req.json()
'''


def get_game_stats(game_id, account):
    """game_id from instance_id_values list"""

    # Destiny2.GetPostGameCarnageReport
    pgcr_path = "/Destiny2/Stats/PostGameCarnageReport/" + game_id
    req = requests.get(default_url + pgcr_path, headers=HEADERS)

    pgcr_info = req.json()

    activity_period = pgcr_info['Response']['period']
    activity_details = pgcr_info['Response']['activityDetails']

    pgcr_entries = pgcr_info['Response']['entries']

    pgcr_player_dict_list = []

    for player in pgcr_entries:
        # player values
        #print(player['values'])
        #player_dict = {}


        # print pgcr extended weapon data
        #print(player['extended']['weapons'])

        player_info = player['player']['destinyUserInfo']
        stats = player['values']


        #weapons_list = player['extended']['weapons']

        '''
        # get list of weapon names for each player
        for weapon in weapons_list:
            print(get_weapon_by_id(weapon['referenceId'], player_info['membershipId']))
        '''
        # compile player info into dictionary
        #if player_info['membershipId'] == user_info['membershipId']:
        if player_info['membershipId'] == account.membership_id:

            player_dict = {'display_name': player_info['displayName'],
                           'membership_id': player_info['membershipId'],
                           'class': player['player']['characterClass'],
                           'score': stats['score']['basic']['value'],
                           'kills': stats['kills']['basic']['value'],
                           'deaths': stats['deaths']['basic']['value'],
                           'assists': stats['assists']['basic']['value'],
                           'avg_score_per_life': stats['averageScorePerLife']['basic']['value'],
                           'opponents_defeated': stats['opponentsDefeated']['basic']['value'],
                           'efficiency': stats['efficiency']['basic']['value'],
                           'kdr': stats['killsDeathsRatio']['basic']['value'],
                           'kda': stats['killsDeathsAssists']['basic']['value'],
                           'standing': stats['standing']['basic']['value'],
                           'team': stats['team']['basic']['value'],
                           'team_score': stats['teamScore']['basic']['value']}

            # append player dictionary to list
            pgcr_player_dict_list.append(player_dict)

            #print(player_dict.keys())
            game_df = pd.DataFrame.from_dict(player_dict, orient='index')
            return game_df.T  # return transposed game stats df
            #return player_dict

    print('User not found in PGCR')


def get_comp_stat_df(account):

    match_ids = get_comp_match_ids(account)

    comp_stats_df = pd.DataFrame()

    for match in match_ids:

        # obtain df of game statistics
        match_stats = get_game_stats(match, account)

        # append each match to df of all match stats
        comp_stats_df = comp_stats_df.append(match_stats, ignore_index=True)

    return comp_stats_df


if __name__ == '__main__':

    pd.set_option('display.max_rows', 100)
    pd.set_option('display.width', 500)
    pd.set_option('display.max_columns', 50)

    my_account = DestinyAccount('Seamusin')

    print(get_comp_stat_df(my_account))

    '''
    comp_match_ids = get_comp_match_ids(my_account)

    game_stats_df = pd.DataFrame()

    # iterate through all comp matches (for 1 character)
    for game in comp_match_ids:

        # obtain df of game statistics
        game_stats = get_game_stats(game, my_account)
        
        # append each game to df of all game stats
        game_stats_df = game_stats_df.append(game_stats, ignore_index=True, sort=True)

    print('\n\n\nDone obtaining match data\n\n\n')

    print(game_stats_df)
    '''






