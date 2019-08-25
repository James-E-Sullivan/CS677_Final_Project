from data_collection import bungie_api as bng
from data_collection import manifest_hash_functions as manifest
import pandas as pd

if __name__ == '__main__':

    pd.set_option('display.max_rows', 100)
    pd.set_option('display.width', 500)
    pd.set_option('display.max_columns', 50)

    my_account = bng.DestinyAccount('Seamusin')

    print(bng.get_comp_stat_df(my_account))

