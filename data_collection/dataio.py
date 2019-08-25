import os
import pandas as pd
import data_collection.bungie_api as bng


#test_df = pd.DataFrame(data=[[0, 1]], columns=['a', 'b'])


def output_match_data(df_matches, name):
    """
    Output DataFrame to csv file
    :param df_matches: Dataframe with Destiny match data
    :param name: name of player (or other signifying string)
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(base_dir, 'match_datasets', name + '.csv')
        df_matches.to_csv(output_file, index=False)

    except Exception as e:
        print(e)
        print('Failed to output match data')

    print('Successfully output match data')


if __name__ == '__main__':

    account_names = ['IX Fall0ut XI',
                     'PureChilly',
                     'Seamusin',
                     'NeutralDefault']

    # output competitive playlist match data for above accounts
    for acct_name in account_names:

        try:
            account = bng.DestinyAccount(acct_name)
            match_df = bng.get_comp_stat_df(account)
            output_match_data(match_df, acct_name)

        except Exception as e:
            print(e)
            print('Failed to obtain user match data')
