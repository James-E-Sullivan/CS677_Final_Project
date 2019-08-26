import pandas as pd
import numpy as np
import copy
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


def logistic_regression_test(df1, df2):
    """
    Predict win/loss values using logistic regression
    :param df1: training set (DataFrame)
    :param df2: prediction set (DataFrame)
    :return: prediction values (numpy ndarray)
    """
    # training data
    x = df1[['kills', 'deaths']].values
    y = df1['standing'].values

    # scale training data
    scaler = StandardScaler()
    scaler.fit(x)
    x = scaler.transform(x)

    # create logistic regression classifier and fit it to training data
    log_reg_classifier = LogisticRegression(solver='lbfgs')
    log_reg_classifier.fit(x, y)

    # prediction data
    x_2 = df2[['kills', 'deaths']].values
    x_2 = scaler.transform(x_2)

    # predict win/loss values for df2 values & return predictions
    prediction = log_reg_classifier.predict(x_2)
    return prediction


def linear_svm_test(df1, df2):
    """
    Predict win/loss values using linear SVM
    :param df1: training set (DataFrame)
    :param df2: prediction set (DataFrame)
    :return: prediction values (numpy ndarray)
    """
    # training data
    x = df1[['kills', 'deaths']].values
    y = df1['standing'].values

    # scale training data
    scaler = StandardScaler()
    scaler.fit(x)
    x = scaler.transform(x)

    # create linear SVM classifier and fit it to training data
    linear_svm_classifier = svm.SVC(kernel='linear')
    linear_svm_classifier.fit(x, y)

    # prediction data
    x_2 = df2[['kills', 'deaths']].values
    scaler.fit(x_2)
    x_2 = scaler.transform(x_2)

    # predict win/loss values for df2 values and return predictions
    prediction = linear_svm_classifier.predict(x_2)
    return prediction


def weapon_type_win_rate(data):

    return data[['standing', 'weapon_type']].groupby(
        ['weapon_type']).mean().reset_index()
