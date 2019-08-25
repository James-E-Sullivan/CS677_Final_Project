import pandas as pd
import numpy as np
import copy
from sklearn import svm
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt


def logistic_regression_test(df1, df2):

    # training data
    x = df1[['kills', 'deaths']].values
    scaler = StandardScaler()
    scaler.fit(x)
    x = scaler.transform(x)
    y = df1['standing'].values

    log_reg_classifier = LogisticRegression(solver='lbfgs')
    log_reg_classifier.fit(x, y)

    # prediction data
    x_2 = df2[['kills', 'deaths']].values
    x_2 = scaler.transform(x_2)
    y_2 = df2['standing'].values

    prediction = log_reg_classifier.predict(x_2)
    return prediction


# this is not a comprehensive dictionary
weapon_type_dict = {'Auto Rifle': 'primary',
                    'Fusion Rifle': 'special',
                    'Grenade Launcher': 'Heavy',
                    'Hand Cannon': 'primary',
                    'Pulse Rifle': 'primary',
                    'Rocket Launcher': 'Heavy',
                    'Scout Rifle': 'primary',
                    'Shotgun': 'special',
                    'Sidearm': 'primary',
                    'Sniper Rifle': 'special',
                    'Submachine Gun': 'primary',
                    'None': 'None'}


def logistic_regression_categorical(df1, df2):



    training_df = copy.copy(df1)

    '''
    training_dummy_df = pd.DataFrame()


    key_list = weapon_type_dict.keys()
    
    for weapon in key_list:

        training_dummy_df[weapon] = np.zeros(len(training_df))

    '''

    training_df['primary'] = training_df.weapon_type.apply(primary_category)
    training_df['special'] = training_df.weapon_type.apply(special_category)
    training_df['heavy'] = training_df.weapon_type.apply(heavy_category)

    print(training_df)

    #print(training_df)

    #input_data = training_df['weapon_type']
    #dummies = pd.get_dummies(input_data)
    #training_dummy_df = training_dummy_df.append(dummies, ignore_index=False, sort=True)
    #print(dummies)

    #print(training_dummy_df)

    X = training_df[['primary', 'special']].values
    print(X)


    le = LabelEncoder()
    Y = le.fit_transform(training_df['standing'].values)
    log_reg_classifier = LogisticRegression()
    log_reg_classifier.fit(X, Y)

    prediction_df = copy.copy(df2)

    prediction_df['primary'] = prediction_df.weapon_type.apply(primary_category)
    prediction_df['special'] = prediction_df.weapon_type.apply(special_category)
    prediction_df['heavy'] = prediction_df.weapon_type.apply(heavy_category)

    X_2 = prediction_df[['primary', 'special']].values

    prediction = log_reg_classifier.predict(X_2)

    print(prediction)
    return prediction





def weapon_type_win_rate(data):

    return data[['standing']].groupby(['weapon_type']).mean().reset_index()


def primary_category(v):

    if weapon_type_dict[v] is 'primary':
        return 1
    else:
        return 0


def special_category(v):

    if weapon_type_dict[v] is 'special':
        return 1
    else:
        return 0


def heavy_category(v):

    if weapon_type_dict[v] is 'heavy':
        return 1
    else:
        return 0


def linear_svm_test(df1, df2):

    # training data
    x = df1[['kills', 'deaths']].values
    scaler = StandardScaler()
    scaler.fit(x)
    x = scaler.transform(x)
    y = df1['standing'].values

    linear_svm_classifier = svm.SVC(kernel='linear')
    linear_svm_classifier.fit(x, y)

    x_2 = df2[['kills', 'deaths']].values
    scaler.fit(x_2)
    x_2 = scaler.transform(x_2)

    prediction = linear_svm_classifier.predict(x_2)

    return prediction




def k_d_linear_regression(df1, df2):

    #x = df1[['kills', 'deaths']].values
    #y = df1['standing'].values  # win/loss labels

    x = df1['kills'].values
    y = df1['deaths'].values

    x = x[:, np.newaxis]  # flip axis of array x

    lin_reg = LinearRegression(fit_intercept=True)
    lin_reg.fit(x, y)

    r_squared = lin_reg.score(x, y)
    slope = lin_reg.coef_[0]
    intercept = lin_reg.intercept_

    plot_regression(x, y, slope, intercept)


def plot_regression(x, y, slope, intercept):
    plt.scatter(x, y, color="blue", marker="o")
    y_pred = slope * x + intercept
    plt.plot(x, y_pred, color='green', lw=3)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()



