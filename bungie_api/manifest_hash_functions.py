import sqlite3
from sqlite3 import Error
import os


def find_id(hash):
    val = int(hash)
    if val and (1 << (32 - 1)) != 0:
        val = val - (1 << 32)

    return val


print(find_id(2957367743))


def create_connection(db_file):
    """
    Create a database connection to the SQLite database
    specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        print('successfully connected')
        return conn
    except Error as e:
        print(e)
        print('connection unsuccessful')
    return None


def select_item(conn, reference_id):

    cur = conn.cursor()
    cur.execute("SELECT json FROM main.DestinyInventoryItemDefinition WHERE id = " + str(reference_id))
    #cur.execute("SELECT name FROM main.sqlite_master WHERE type='table'")
    rows = cur.fetchall()
    for row in rows:
        print(row)


#DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "world_sql_content_.sqlite3")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


input_dir = os.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[:-2])
print(input_dir)
db_dir = "/CS677_Final_Project/manifests"

db_name = "world_sql_content_.sqlite3"
#db_path = os.path.join(input_dir, db_dir, db_name)

db_path = os.path.join(BASE_DIR, "manifests", db_name)
print(db_path)

manifest_conn = create_connection(db_path)
select_item(manifest_conn, -1337599553)



