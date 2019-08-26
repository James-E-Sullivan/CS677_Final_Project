import os
import data_collection.bungie_api as bng


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
    '''Run this to obtain new match data - either by updating
    existing account files, or by adding new account files (which would
    involve adding new names to account_names).'''

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
