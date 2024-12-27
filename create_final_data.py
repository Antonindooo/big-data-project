"""
File use to create final data like monthly, yearly or daily one from data/intermediate dataframe
and save all these new data to data/final
"""
from src.transformation.constants import SYMBOLS

import findspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql import Window
from IPython.display import display


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

spark = init_spark_session()
spark_df = spark.read.csv(path="data/intermediate/cleaned_df.csv", header=True, inferSchema=True, ignoreLeadingWhiteSpace=True)

def calculate_return_rate(spark_df, symbols):

    # Add temporal columns for Year, Month, and Week based on the "Date" column
    spark_df = spark_df.withColumn("Year", year("Date"))

    for symbol in symbols:
        open_col = f"Open_{symbol}"
        close_col = f"Close_{symbol}"

        # Calculate the yearly return rate
        return_rate_year = spark_df.groupBy("Year").agg(
            first(open_col).alias("Starting_Price_year"),
            last(close_col).alias("Ending_Price_year")
        ).withColumn(
            f"return_rate_{symbol}_year",
            (col("Ending_Price_year") - col("Starting_Price_year")) / col("Starting_Price_year")
        ).orderBy("Year")
    # Retourner le DataFrame avec les nouvelles colonnes de taux de retour
    return return_rate_year
return_rate = calculate_return_rate(spark_df, ["AAPL"])
return_rate.toPandas().to_csv("data/final/return_rate.csv")
# Supprimer la première colonne "_c0" qui est vide
spark_df = spark_df.drop("_c0")
spark_df = spark_df.withColumn("Date", to_date("Date", "yyyy-MM-dd"))

# Filtrer pour ne conserver que les dates après 2018
spark_df_mv = spark_df.filter(col("Date") > "2018-01-01")
def calculate_moving_average(spark_df, column_name, num_periods):
    #define a window that includes the current row and the previous (num_periods - 1) rows
    window_spec = Window.orderBy("Date").rowsBetween(-(num_periods - 1), 0)

    # Add the moving average column
    moving_avg_col = f"{column_name}_Moving_Avg_{num_periods}"
    spark_df = spark_df.withColumn(
        moving_avg_col,
        avg(col(column_name)).over(window_spec)
    )
    return spark_df
choosed_col = "Close_AAPL"
number_of_periods= 50
mv_avg = calculate_moving_average(spark_df_mv, choosed_col, number_of_periods)
number_of_periods= 200
mv_avg = calculate_moving_average(mv_avg, choosed_col, number_of_periods)
mv_avg.toPandas().to_csv("data/final/mv_avg.csv")
number_of_periods= 20
for i, symbol in enumerate(SYMBOLS):
    choosed_col = f"Close_{symbol}"
    if i == 0:
        mv_avg_20 = calculate_moving_average(spark_df, choosed_col, number_of_periods)
    else:
        mv_avg_20 = calculate_moving_average(mv_avg_20, choosed_col, number_of_periods)

mv_avg_20.toPandas().to_csv("data/final/mv_avg_20.csv")


spark_df_crisis = spark_df.filter(col("Date") > "2022-01-01")
spark_df_crisis = spark_df_crisis.filter(col("Date") < "2023-01-01")
spark_df_crisis.toPandas().to_csv("data/final/after_crisis.csv")


def calculate_monthly_changes(spark_df, symbols):
    # Add columns for temporal periods (Year, Month, and Week)
    spark_df = spark_df.withColumn("Year", year("Date")) \
                       .withColumn("Month", month("Date"))
    # Initialisation d'une liste pour stocker les résultats partiels
    results = []
    for symbol in symbols:
        close_col = f"Close_{symbol}"

        if close_col in spark_df.columns:
            # Calculate the average closing prices grouped by Year and Month
            avg_prices_month = spark_df.groupBy("Year", "Month").agg(
                {close_col: "avg"}
            ).withColumnRenamed(f"avg({close_col})", f"Avg_Close_{symbol}_Month")

            # Define a window specification ordered by Year and Month
            window_spec = Window.orderBy("Year", "Month")

            # Add a column for the average closing price of the previous month
            avg_prices_month = avg_prices_month.withColumn(
                f"Avg_Close_{symbol}_Prev_Month",
                lag(f"Avg_Close_{symbol}_Month").over(window_spec)
            )

            # Calculate the monthly change by subtracting the previous month's average from the current month's average
            avg_prices_month = avg_prices_month.withColumn(
                f"Monthly_Change_{symbol}",
                col(f"Avg_Close_{symbol}_Month") - col(f"Avg_Close_{symbol}_Prev_Month")
            )
            # Joindre les résultats au DataFrame d'origine
            spark_df = spark_df.join(
                avg_prices_month,
                on=["Year", "Month"],
                how="left"
            )
    filtered_df = spark_df.select(["Year", "Month"] + [col(c) for c in spark_df.columns if c.startswith("Monthly")]).distinct().orderBy(["Year","Month"])

    return filtered_df
# Appel de la fonction
Monthly_change = calculate_monthly_changes(spark_df, SYMBOLS)
# Sauvegarde des résultats
Monthly_change.toPandas().to_csv("data/final/monthly_change.csv", index=False)
