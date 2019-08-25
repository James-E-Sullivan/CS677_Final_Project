import pandas as pd
import os, copy
import data_analysis.k_d_logistic_regression as kdlr
import help_package.help_functions as hf
import numpy as np



def open_csv_as_df(account_name):

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_dir = 'data_collection/match_datasets'
        data_file = os.path.join(base_dir, file_dir, account_name + '.csv')
        data = pd.read_csv(data_file)
        return data
    except FileNotFoundError as e:
        print(e)
        print('Could not find', account_name + '.csv')
    return None


if __name__ == '__main__':

    hf.show_more_df()

    account_names = ['IX Fall0ut XI',
                     'PureChilly',
                     'Seamusin',
                     'NeutralDefault']

    unique_weapon_types = []
    for name in account_names:

        my_df = open_csv_as_df(name)
        my_df = my_df.fillna('None')

        training_index = len(my_df) // 2
        training_index_list = [i for i in range(0, len(my_df) // 2)]
        prediction_index_list = [i for i in range(len(my_df) // 2, len(my_df))]

        df1 = my_df.iloc[training_index_list]
        df1 = copy.copy(df1)
        df2 = my_df.iloc[prediction_index_list]
        df2 = copy.copy(df2)


        log_reg_predictions = kdlr.logistic_regression_test(df1, df2)

        svm_predictions = kdlr.linear_svm_test(df1, df2)

        '''
        df2 = df2.append(log_reg_df, ignore_index=False, sort=False)
        df2 = df2.append(svm_df, ignore_index=False, sort=False)
        '''

        df2['log_reg_pred'] = log_reg_predictions
        df2['svm_pred'] = svm_predictions

        #print(df2)

        #unique_weapons = pd.unique(my_df['weapon_type'].values)

        print(len(df1))
        print(len(df2))

        df2.dropna()
        print(len(df2))

        df2['w_type_pred'] = kdlr.logistic_regression_categorical(df1, df2)

        print(df2)

        '''
        for weapon_type in unique_weapons:
            unique_weapon_types.append(weapon_type)
        '''

        #print(kdlr.weapon_type_win_rate(my_df))

    #unique_weapon_types = np.unique(np.array(unique_weapon_types))
    #print(unique_weapon_types)




