import findspark
from pyspark.sql import SparkSession, DataFrame
import pandas as pd
import yfinance as yf
from pyspark.sql.functions import *
from pyspark.sql import Window
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns


# def init_spark_session():
#     findspark.init("C:\Spark")
#     nasdaq_app = "Nasdaq_tech_stocks "

#     spark = (
#         SparkSession
#         .builder
#         .appName(nasdaq_app)
#         .getOrCreate()
#     )
#     return spark


def download_dataset(symbol: list[str], start_date: str, end_date: str) -> pd.DataFrame:
    """
    This function takes a stock symbol and a date range (start and end dates) to download historical data
    """

    # Load the stock data into a pandas DataFrame using yfinance
    panda_df = yf.download(symbol, start=start_date, end=end_date)
    panda_df.reset_index(inplace=True)

    # Convert the pandas DataFrame into a Spark DataFrame
    # spark_df = spark_session.createDataFrame(panda_df)
    return panda_df

#df = download_dataset(symbols, "2001-01-01", "2024-12-31")

def rename_columns(df: pd.DataFrame):

    # for col in df.columns:
    #     # Retain "Date" column as is and simplify the other column names
    #     if col == "('Date', '')":
    #         df = df.withColumnRenamed(col, "Date")

    #     # Replace special characters and remove spaces
    #     else:
    #         new_col_name = (
    #             col.replace("(", "")
    #                .replace(")", "")
    #                .replace("'", "")
    #                .replace(", ", "_")
    #                .replace(" ", "_")
    #         )
    #         df = df.withColumnRenamed(col, new_col_name)

    # # Convert the "Date" column to a date format
    # df = df.withColumn("Date", to_date("Date"))
    # df.show()
    # df.printSchema()
    df.columns = ["Date"] + ['_'.join(col).strip() for col in df.columns.values if col != ("Date", "")]
    return df

#spark_df = rename_columns(df)

def filter_on_symbol(symbols, spark_df):
    columns_to_keep = []
    for col in spark_df.columns:
        if col.endswith(tuple(symbols)) or col == "Date":
            columns_to_keep.append(col)
    # return spark_df.select(*columns_to_keep)
    return spark_df[columns_to_keep]