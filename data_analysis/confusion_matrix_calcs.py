"""
Functions for calculating accuracy, true/false positive/negative rates, and
for calculating confusion matrices
"""

import numpy as np


def get_acc(vector):
    """
    Returns 1's for accurate prediction, otherwise returns 0
    :param vector: vector containing (actual, predicted) values
    :return: 1 or 0
    """
    if vector[0] == vector[1]:
        return 1
    else:
        return 0


def tp(vector):
    """
    Compares actual vs predicted label values.
    Returns 1 only if result is a true positive
    :param vector: vector containing (actual, predicted) values
    :return: 1 or 0
    """
    if vector[0] == 1 and vector[1] == 1:
        return 1
    else:
        return 0


def fp(vector):
    """
    Compares actual vs predicted label values.
    Returns 1 only if result is a false positive
    :param vector: vector containing (actual, predicted) values
    :return: 1 or 0
    """
    if vector[0] == 0 and vector[1] == 1:
        return 1
    else:
        return 0


def tn(vector):
    """
    Compares actual vs predicted label values.
    Returns 1 only if result is a true negative
    :param vector: vector containing (actual, predicted) values
    :return: 1 or 0
    """
    if vector[0] == 0 and vector[1] == 1:
        return 1
    else:
        return 0


def fn(vector):
    """
    Compares actual vs predicted label values.
    Returns 1 only if result is a false negative
    :param vector: vector containing (actual, predicted) values
    :return: 1 or 0
    """
    if vector[0] == 1 and vector[1] == 0:
        return 1
    else:
        return 0


def confusion_matrix(tp_sum, fp_sum, tn_sum, fn_sum):
    """
    :param tp_sum: # true positives
    :param fp_sum: # false positives
    :param tn_sum: # true negatives
    :param fn_sum: # false negatives
    :return:
    """
    return np.array([[tn_sum, fp_sum], [fn_sum, tp_sum]])