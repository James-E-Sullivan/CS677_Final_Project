import pandas as pd
import os, copy
import data_analysis.analysis_functions as af
import help_package.help_functions as hf
import data_analysis.confusion_matrix_calcs as cm
import numpy as np


def open_csv_as_df(account_name):
    """
    Open csv from data_collection/match_datasets as a DataFrame
    :param account_name: Name of player account and csv file
    :return: DataFrame with Destiny 2 match data
    """
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


def analyze_predictions(data, col_name):
    """
    Output accuracy, confusion matrix, True Positive/Negative Rates
    to the console
    :param data: DataFrame with win/loss data and a predicted win/loss value
    :param col_name: Column name corresponding to prediction method
    """
    # analyze logistic regression predictions
    accuracy = data[col_name].sum() / data[col_name].count()
    print('Accuracy of predictions: ', accuracy)

    data['tp'] = data[['standing', col_name]].apply(cm.tp, axis=1)
    data['fp'] = data[['standing', col_name]].apply(cm.fp, axis=1)
    data['tn'] = data[['standing', col_name]].apply(cm.tn, axis=1)
    data['fn'] = data[['standing', col_name]].apply(cm.fn, axis=1)

    # compute sum of true/false positive/negative values
    tp_sum = data.tp.sum()
    fp_sum = data.fp.sum()
    tn_sum = data.tn.sum()
    fn_sum = data.fn.sum()

    # compute confusion matrix
    confusion_matrix_result = cm.confusion_matrix(tp_sum, fp_sum, tn_sum,
                                                  fn_sum)
    print('\nConfusion Matrix: \n', confusion_matrix_result)

    # calculate true positive and true negative rates
    try:
        tpr = tp_sum / (tp_sum + fp_sum)
    except FloatingPointError:
        # dividing by 0 will result in FloatingPointError
        tpr = 0

    try:
        tnr = tn_sum / (tn_sum + fp_sum)
    except FloatingPointError:
        # dividing by 0 will result in FloatingPointError
        tnr = 0

    # true positive and negative rates
    print('\nTrue Positive Rate: ', tpr)
    print('True Negative Rate: ', tnr)


if __name__ == '__main__':

    hf.show_more_df()

    account_names = ['IX Fall0ut XI',
                     'PureChilly',
                     'Seamusin',
                     'NeutralDefault']

    for name in account_names:

        # open csv file corresponding to name as a DataFrame
        my_df = open_csv_as_df(name)
        my_df = my_df.fillna('None')  # fill NaN values with 'None'

        # split df into two approximately equal dfs
        training_index = len(my_df) // 2
        training_index_list = [i for i in range(0, len(my_df) // 2)]
        prediction_index_list = [i for i in range(len(my_df) // 2, len(my_df))]

        df1 = my_df.iloc[training_index_list].reset_index()
        df1 = copy.copy(df1)
        df2 = my_df.iloc[prediction_index_list].reset_index()
        df2 = copy.copy(df2)

        # get win/loss prediction values via logistic regression
        log_reg_predictions = af.logistic_regression_test(df1, df2)

        # get win/loss prediction values via linear SVM
        svm_predictions = af.linear_svm_test(df1, df2)

        # add predictions values as columns in df2
        df2['log_reg_pred'] = log_reg_predictions
        df2['svm_pred'] = svm_predictions

        # calculate accuracy of predictions
        df2['log_reg_acc'] = df2[['standing', 'log_reg_pred']].apply(cm.get_acc,
                                                                     axis=1)
        df2['svm_acc'] = df2[['standing', 'svm_pred']].apply(cm.get_acc, axis=1)

        # output analysis of predictions
        print('\n\n________Analysis of', name, 'game data predictions________')

        print('\n--Logistic Regression Analysis--')
        analyze_predictions(df2, 'log_reg_acc')

        print('\n--Linear SVM Analysis--')
        analyze_predictions(df2, 'svm_acc')

        # Create df with loss-rate (standing mean) grouped by weapon type
        win_rate_df = af.weapon_type_win_rate(my_df)

        # Add win-rate columns (1 - loss rate)
        win_rate_df['win_rate'] = win_rate_df['standing'].apply(lambda a: 1 - a)

        # create df with only the max win-rate weapons
        max_win_rate = win_rate_df.win_rate.max()
        best_items_df = win_rate_df.loc[win_rate_df.win_rate == max_win_rate]

        # output weapon types with best win rates
        #    * note that the only listed weapon type per game is that which had
        #    * accounted for the most enemies defeated
        print('\nHighest win rate for ' + name +
              ' when the majority of\n'
              'enemies are defeated with the following weapon types: ')

        for item in best_items_df.weapon_type.values:
            print(item)

