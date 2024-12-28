"""
File use to load data from yfinance API, preprocess it and save in data/intermediate
"""
from constants import SYMBOLS

import findspark
from pyspark.sql import SparkSession, DataFrame
import pandas as pd
import yfinance as yf
from pyspark.sql.functions import *
from pyspark.sql import Window
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns


def init_spark_session()-> SparkSession:
    findspark.init("C:\Spark")
    nasdaq_app = "Nasdaq_tech_stocks "

    spark = (
        SparkSession
        .builder
        .appName(nasdaq_app)
        .getOrCreate()
    )
    return spark


def download_dataset(symbol: list[str], start_date: str, end_date: str, spark_session):
    """
    This function takes a stock symbol and a date range (start and end dates) to download historical data
    """

    # Load the stock data into a pandas DataFrame using yfinance
    panda_df = yf.download(symbol, start=start_date, end=end_date)
    panda_df.reset_index(inplace=True)
    for symbols in SYMBOLS:
        df_for_each = yf.download(symbols, start=start_date, end=end_date)
        df_for_each.reset_index(inplace=True)
        df_for_each.to_csv(f"data/intermediate/original_{symbols}.csv")
    # Convert the pandas DataFrame into a Spark DataFrame
    spark_df = spark_session.createDataFrame(panda_df)
    return spark_df

df = download_dataset(SYMBOLS, "2000-01-01", "2024-12-31", spark_session=init_spark_session())

def rename_columns(df):

    for col in df.columns:
        # Retain "Date" column as is and simplify the other column names
        if col == "('Date', '')":
            df = df.withColumnRenamed(col, "Date")

        # Replace special characters and remove spaces
        else:
            new_col_name = (
                col.replace("(", "")
                   .replace(")", "")
                   .replace("'", "")
                   .replace(", ", "_")
                   .replace(" ", "_")
            )
            df = df.withColumnRenamed(col, new_col_name)

    # Convert the "Date" column to a date format
    df = df.withColumn("Date", to_date("Date"))

    return df

spark_df = rename_columns(df)

def cleaning(df):
    for colu in df.columns:
        if colu == "Date":
            continue
        # Replace "NaN" values with None and cast other values to float
        else:
            df = df.withColumn(colu, when(col(colu) == "NaN", None).otherwise(col(colu).cast("float")))
    return df

spark_df = cleaning(spark_df)
spark_df.toPandas().to_csv("data/intermediate/cleaned_df.csv")
