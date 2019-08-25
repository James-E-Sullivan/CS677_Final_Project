import sqlite3
from sqlite3 import Error
import os
import json


def find_id(hash_id):
    val = int(hash_id)
    if (val and (1 << (32 - 1))) != 0:
        val = val - (1 << 32)
    return val


def create_connection(db_file):
    """
    Create a database connection to the SQLite database
    specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        print('Successfully connected to database')
        return conn
    except Error as e:
        print(e)
        print('Connection unsuccessful')
    return None


def select_item(conn, reference_id):
    """
    Return item json from Destiny manifest
    :param conn: sqlite3 connection to manifest db
    :param reference_id: item referenceId (aka hashId)
    :return: item json dict
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT json FROM main.DestinyInventoryItemDefinition WHERE id = " +
            str(reference_id))

        rows = cur.fetchall()
        item_json = rows[0][0]  # item json string from db

        item_dict = json.loads(item_json)  # parse json string into dict

        return item_dict
    except Error as e:
        print(e)
    return None


def select_json_item(conn, reference_id):

    try:
        cur = conn.cursor()

        cur.execute("SELECT json FROM main.DestinyInventoryItemDefinition")

        rows = cur.fetchall()
        return rows
    except Error as e:
        print(e)
    return None


hashes = {'DestinyAchievementDefinition': 'achievementHash',
          'DestinyActivityDefinition': 'activityHash',
          'DestinyActivityGraphDefinition': 'activityGraphHash',
          'DestinyActivityModeDefinition': 'activityModeHash',
          'DestinyActivityModifierDefinition': 'activityModifierHash',
          'DestinyActivityTypeDefinition': 'activityTypeHash',
          'DestinyBondDefinition': 'bondHash',
          'DestinyChecklistDefinition': 'checklistHash',
          'DestinyClassDefinition': 'classHash',
          'DestinyCollectibleDefinition': 'collectibleHash',
          'DestinyDamageTypeDefinition': 'damageTypeHash',
          'DestinyDestinationDefinition': 'destinationHash',
          'DestinyEnemyRaceDefinition': 'enemyRaceHash',
          'DestinyEquipmentSlotDefinition': 'equipmentSlotHash',
          'DestinyFactionDefinition': 'factionHash',
          'DestinyGenderDefinition': 'genderHash',
          'DestinyHistoricalStatsDefinition': 'historicalStatsHash',
          'DestinyInventoryBucketDefinition': 'inventoryBucketHash',
          'DestinyInventoryItemDefinition': 'itemHash',
          'DestinyItemCategoryDefinition': 'itemCategoryHash',
          'DestinyItemTierTypeDefinition': 'itemTierTypeHash',
          'DestinyLocationDefinition': 'locationHash',
          'DestinyLoreDefinition': 'loreHash',
          'DestinyMaterialRequirementSetDefinition': 'materialHash',
          'DestinyMedalTierDefinition': 'medalHash',
          'DestinyMilestoneDefinition': 'milestoneHash',
          'DestinyObjectiveDefinition': 'objectiveHash',
          'DestinyPlaceDefinition': 'placeHash',
          'DestinyPlugSetDefinition': 'plugSetHash',
          'DestinyPresentationNodeDefinition': 'presentationNodeHash',
          'DestinyProgressionDefinition': 'progressionHash',
          'DestinyProgressionLevelRequirementDefinition': 'levelRequirementHash',
          'DestinyRaceDefinition': 'raceHash',
          'DestinyRecordDefinition': 'recordHash',
          'DestinyReportReasonCategoryDefinition': 'reportHash',
          'DestinyRewardSourceDefinition': 'rewardSourceHash',
          'DestinySackRewardItemListDefinition': 'sackRewardHash',
          'DestinySandboxPatternDefinition': 'sandboxPatternHash',
          'DestinySandboxPerkDefinition': 'perkHash',
          'DestinySeasonDefinition': 'seasonHash',
          'DestinySocketCategoryDefinition': 'socketCategoryHash',
          'DestinySocketTypeDefinition': 'socketTypeHash',
          'DestinyStatDefinition': 'statHash',
          'DestinyStatGroupDefinition': 'statGroupHash',
          'DestinyTalentGridDefinition': 'talentGridHash',
          'DestinyUnlockDefinition': 'unlockHash',
          'DestinyVendorDefinition': 'vendorHash',
          'DestinyVendorGroupDefinition': 'vendorGroupHash'}


hashes_trunc = {'DestinyInventoryItemDefinition': 'itemHash'}


def build_item_dict(hash_dict):

    # connect to manifest
    db_path = get_db_path()
    conn = create_connection(db_path)

    # create cursor object
    cur = conn.cursor()

    all_data = {}
    for table in hash_dict.keys():

        # get list of jsons from table
        cur.execute("SELECT json FROM " + table)
        print('Generating ' + table + ' Dictionary')

        # returns list of tuples - first item in each tuple is the json
        items = cur.fetchall()

        # create list of jsons
        item_jsons = [json.loads(item[0]) for item in items]

        # create a dictionary with hashes as keys & jsons as values
        item_dict = {}
        hash_name = hash_dict[table]
        for item in item_jsons:
            item_dict[item['hash']] = item

        # add dict to all_data using the name of table as key
        all_data[table] = item_dict

    print('Dictionary Generated')
    return all_data


def item_json_by_hash(hash_id, item_db_dict):
    """
    Return the json dictionary for item w/ corresponding hash ID.
    Requires user to create/load item_db_dict into this function.
    :param hash_id: item hash ID value (referenceId)
    :param item_db_dict: dict w/ {hash: json_dict} pairs - use
    build_item_dict() to create this dict
    :return: json dict for only the item with matching hash_id
    """
    try:
        return item_db_dict[hash_id]
    except Exception as e:
        print(e)
        print('hash_id not in item dict')
    return None


def name_type_by_hash(hash_id, item_db_dict):
    """
    Return the name and type of item, given a hash_id. Queries
    item_db_dict.
    :param hash_id:
    :param item_db_dict:
    :return:
    """
    try:
        item_json = item_json_by_hash(hash_id, item_db_dict)
        item_name = item_json['displayProperties']['name']
        item_type = item_json['itemTypeDisplayName']
        return tuple([item_name, item_type])
    except Exception as e:
        print(e)
        print('issue getting item name and type for hash_id ' + str(hash_id))


def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = "world_sql_content_.sqlite3"
    return os.path.join(base_dir, "manifests", db_name)


def get_item_dict(reference_id):

    db_path = get_db_path()
    manifest_conn = create_connection(db_path)
    item_id = find_id(reference_id)
    item_dict = select_item(manifest_conn, item_id)
    return item_dict


def name_and_type(reference_id):

    try:
        weapon_dict = get_item_dict(reference_id)
        weapon_name = weapon_dict['displayProperties']['name']
        weapon_type = weapon_dict['itemTypeDisplayName']
        return tuple([weapon_name, weapon_type])

    except Exception as e:
        print(e)
        print('issue getting weapon name and type')
    return None




