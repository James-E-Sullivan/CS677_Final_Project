import pandas as pd
import os


def show_more_df():
    """allow df prints to display each column"""
    pd.set_option('display.max_rows', 100)
    pd.set_option('display.width', 500)
    pd.set_option('display.max_columns', 50)

