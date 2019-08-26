import pandas as pd
import numpy as np
import copy
from sklearn import svm
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


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

    training_df['primary'] = training_df.weapon_type.apply(primary_category)
    training_df['special'] = training_df.weapon_type.apply(special_category)
    training_df['heavy'] = training_df.weapon_type.apply(heavy_category)

    print(training_df)

    X = training_df[['primary', 'special', 'heavy']].values
    print(X)

    le = LabelEncoder()
    Y = le.fit_transform(training_df['standing'].values)
    log_reg_classifier = LogisticRegression()
    log_reg_classifier.fit(X, Y)

    prediction_df = copy.copy(df2)

    prediction_df['primary'] = prediction_df.weapon_type.apply(primary_category)
    prediction_df['special'] = prediction_df.weapon_type.apply(special_category)
    prediction_df['heavy'] = prediction_df.weapon_type.apply(heavy_category)

    X_2 = prediction_df[['primary', 'special', 'heavy']].values

    prediction = log_reg_classifier.predict(X_2)

    print(prediction)
    return prediction


def weapon_type_win_rate(data):

    return data[['standing', 'weapon_type']].groupby(['weapon_type']).mean().reset_index()


def most_used_weapons(data):

    return data[['weapon_name']].groupby('weapon_name').count().reset_index()


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







