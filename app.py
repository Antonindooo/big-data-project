import streamlit as st
import pandas as pd
import mplfinance as mpf
from constants import SYMBOLS
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt


def filter_on_symbol(symbols, spark_df):
    columns_to_keep = []
    for col in spark_df.columns:
        if (col.endswith(tuple(symbols)) and (col.startswith("Close"))) or col == "Date":
            columns_to_keep.append(col)
    return spark_df[columns_to_keep]

def calculate_correlation(spark_df, stock1, stock2):
    if stock1 in spark_df.columns and stock2 in spark_df.columns:
        # Calculer la corrélation
        correlation = spark_df[stock1].corr(spark_df[stock2])
        return correlation
    else:
        raise ValueError(f"Une ou les deux colonnes ({stock1}, {stock2}) ne sont pas présentes dans le DataFrame.")


st.write("# Smart Insights for Strategic Investments")
st.write("")


# 1st insight

def understang_the_graph():
    st.write("### Trend Analysis Through Candlestick Visualization")
    st.write("This interactive chart allows you to select a company and analyze its stock trend through candlestick patterns. It helps identify market tendencies for better investment decisions.")
    #interactive widget in order to choose which graph we want to plot
    new_select = st.radio(
        label="Select a Company to Visualize the Stock Trend :",
        options=SYMBOLS,
        key="radio_1"  # We have to use a unique because I am gonna use several radio widget
    )

    # Loading the CSV file of the selected company
    df = pd.read_csv(f"data/intermediate/original_{new_select}.csv")

    # Convert the date into the correct format
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    start_date = '2024-09-01'
    end_date = '2025-01-01'

    # We just want to see the last stock variation 
    df = df.loc[(df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))]

    # Convert all the columns into numerci type to avoid errors
    df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
    df['High'] = pd.to_numeric(df['High'], errors='coerce')
    df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    
    
    # Create a nice graphic thanks to the mplfinance library
    fig, axes = mpf.plot(df.tail(100), type='candle', style='yahoo', volume=True, returnfig=True)
    st.write("\n")
    st.write("**Stock Trend Analysis Since September 1st 2024**")

    # plot the graph in streamlit
    st.pyplot(fig)

    if new_select == "AAPL":
        st.write("The trend of Apple is currently positive, which may indicate a buying opportunity. The investor should consider buying Apple.")
    elif new_select == "MSFT":
        st.write("The trend of Microsoft is stable, indicating low volatility. The investor should hold Microsoft for now.")
    elif new_select == "AMZN":
        st.write("The trend of Amazon is currently positive, which may indicate a buying opportunity. The investor should consider buying Amazon.")
    elif new_select == "META":
        st.write("The trend of Meta is stable, indicating low volatility. The investor should hold Meta for now.")
    elif new_select == "ZM":
        st.write("The trend of Zoom is currently positive, which may indicate a buying opportunity. The investor should consider buying Zoom.")

understang_the_graph()

# 2nd insight

def return_rate():
    #loading the return rate csv file
    df_return_rate = pd.read_csv("data/final/return_rate.csv")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("### Apple : A Resilient Growth Stock with Cyclical Recoveries")
    st.write("In this insight, we will analyze the evolution of Apple's return rates over the years, identifying key patterns and trends that reflect the stock's performance, resilience, and growth potential.")

    #Creating the figure with plotly library
    fig = go.Figure()
    # First Moving Average
    fig.add_trace(go.Scatter(
        x=df_return_rate['Year'],
        y=df_return_rate['return_rate_AAPL_year'],
        mode='lines',
        line=dict(color='blue', width=2)
    ))
    # Mise en page
    fig.update_layout(
        title="Evolution of Apple's Return Rate Over the Years",
        xaxis_title="Years",
        yaxis_title="Return rate",
        template='plotly_white',
        legend=dict(
            title="Legend",
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.2
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    st.write("Apple's stock price has significantly increased over the years. In fact, in 2001, the closing price was 0.391071, whereas by 2020, it had reached 132.69.")
    st.write("By analyzing the graph, we can identify years with very high return rates:")
    st.write("- 2004: +198%\n - 2007: +129%\n - 2009: +145%\n - 2019: +92%")
    st.write("These years coincide with major product launches and economic events:")
    st.write("- 2004: Launch of the iPod Mini.\n - 2007: Launch of the first iPhone.\n - 2009: Economic recovery following the 2008 global financial crisis.\n - 2019: Launch of the iPhone 11, a major commercial success.")
    st.write("We also observe 3 years with negative return rates:")
    st.write("- 2002: -35%\n - 2008: -57%\n - 2022: -26%")
    st.write("These declines are often linked to global crises (e.g., the 2008 financial crisis), war (e.g., the 2022 Russian-Ukrainian war), or slower product performance and fewer significant launches by Apple.")
    st.write("After each year of decline, Apple experienced a strong recovery:")
    st.write("- In 2003, the return rate was +48%.\n - In 2009, the return rate was +145%.\n - In 2023, the return rate was +47%.")
    st.write("In the early 2000s, the return rates showed significant volatility, ranging from -35% in 2002 to +198% in 2004, but they became more stable after 2010.")
    st.write("Based on the information provided, we can conclude that Apple is a strong long-term growth stock, demonstrating remarkable resilience and bouncing back strongly after challenging periods. However, it's important to note that Apple's performance can be sensitive to current market conditions and news events. Looking ahead, if there is a significant decline in return rates in the future, it could present an attractive investment opportunity.")

return_rate()

# 3rd insight

def moving_average():
    #loading the moving average dataframe
    df_moving_average = pd.read_csv("data/final/mv_avg.csv")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    # Créer la figure Plotly
    fig = go.Figure()
    # Ajouter la première courbe (Close_AAPL_Moving_Avg_200)
    fig.add_trace(go.Scatter(
        x=df_moving_average['Date'],
        y=df_moving_average['Close_AAPL_Moving_Avg_200'],
        mode='lines',
        name='200-Day Moving Averages',
        line=dict(color='blue', width=2) 
    ))
    #2nd one
    fig.add_trace(go.Scatter(
        x=df_moving_average['Date'],
        y=df_moving_average['Close_AAPL'],
        mode='lines',
        name='Closin Price',
        line=dict(color='green', width=2)  
    ))

    # 3rd one
    fig.add_trace(go.Scatter(
        x=df_moving_average['Date'],
        y=df_moving_average['Close_AAPL_Moving_Avg_50'],
        mode='lines',
        name='50-Day Moving Averages',
        line=dict(color='orange', width=2) 
    ))

    #layout
    fig.update_layout(
        title="Apple's Closing Price with 50-Day and 200-Day Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price",
        template='plotly_white',
        legend=dict(
            title="Legend",
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.2
        )
    )
    st.write("### Understanding the Golden Cross Phenomenon")
    st.write("The Golden Cross happens when a stock's short-term moving average crosses above its long-term moving average. This is often seen as a bullish signal, showing potential for future growth. Let's see how this applies to our data.")
    st.write("For this example, we will focus on Apple. To analyze its closing price trend, we calculate two moving averages: a 50-day short-term MA and a 200-day long-term MA.")
    st.write("We then plot both curves on the same graph to visualize the trend.")
    
    st.plotly_chart(fig, use_container_width=True)

    st.write("After plotting the curves, we can proceed with the analysis. The **Death Cross** occurs when the 200-day moving average (MA-200) crosses above the 50-day moving average (MA-50), signaling a potential bearish trend. In 2019, we observe that this crossover took place, and Apple’s stock subsequently experienced a decline.")
    st.write("Approximately six months later, the **Golden Cross** occurred, when the MA-50 crossed above the MA-200. This is a widely recognized bullish signal, often indicating the start of an upward trend. Following the Golden Cross, Apple’s stock surged, reflecting strong investor confidence and market optimism.")
    st.write("The **Death Cross** can often be a signal to sell or reduce exposure to the stock, as it suggests a potential downward trend. Investors may choose to exit positions or avoid new purchases until the trend shows signs of reversing.")
    st.write("Conversely, the **Golden Cross** is seen as a buy signal, especially when accompanied by strong trading volume, suggesting upward momentum. Investors often use this signal to enter the stock, expecting price increases.")
    st.write("The Death Cross followed by the Golden Cross in 2019-2020 illustrates how moving averages can be key indicators for market trends. Investors can use these crossovers to identify potential entry or exit points. For instance, the Golden Cross was a strong signal to buy Apple stock, which later delivered significant returns.")
    st.write("Additionally, another Golden Cross occurred in March 2023, followed by another one in June 2024, further confirming positive market sentiment during those periods.")
    st.write("Source: \n https://academy.youngplatform.com/fr/trading/moyennes-mobiles-golden-cross-death-cross/")

moving_average()

# 4th insight

def diversification():
    spark_df = pd.read_csv("data/intermediate/cleaned_df.csv")

    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("### The Importance of Portfolio Diversification")
    st.write("In this insight, we will explore the importance of portfolio diversification by analyzing the correlation between the stock prices of two companies.")


    selected_symbol_1 = st.radio(
        label="Select the first company to observe :",
        options=SYMBOLS
    )

    # Filtrer les options pour exclure le premier choix
    remaining_symbols = [symbol for symbol in SYMBOLS if symbol != selected_symbol_1]

    # Sélection du deuxième choix avec une seconde case
    selected_symbol_2 = st.radio(
        label="Select the second company to observe:",
        options=remaining_symbols
    )

    # Stocker les deux sélections
    selected_symbols = [selected_symbol_1, selected_symbol_2]
    filtered_df = filter_on_symbol(selected_symbols, spark_df)

    fig = go.Figure()
    # Ajouter une trace pour chaque symbole sélectionné
    for symbol in selected_symbols:
        column_name = f"Close_{symbol}"
        if column_name in filtered_df.columns:
            fig.add_trace(go.Scatter(
                x=filtered_df['Date'],  # Axe des x
                y=filtered_df[column_name],  # Axe des y
                mode='lines',  # Mode lignes
                name=symbol,  # Nom pour la légende
                line=dict(width=2)  # Personnalisation des lignes
            ))

    # Mettre à jour la mise en page
    fig.update_layout(
        title="Closing Price evolution",
        xaxis_title="Years",
        yaxis_title="Closing Price",
        template='plotly_white',
        legend=dict(
            title="Legend",
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.2
        )
    )
    stock1 = f"Close_{selected_symbol_1}"
    stock2 = f"Close_{selected_symbol_2}"
    correlation = calculate_correlation(filtered_df, stock1, stock2)

    st.plotly_chart(fig, use_container_width=True)
    if selected_symbol_1 == "AAPL":
        selected_symbol_1 = "Apple"
    if selected_symbol_1 == "MSFT":
        selected_symbol_1 = "Microsoft"
    if selected_symbol_1 == "ZM":
        selected_symbol_1 = "Zoom"
    if selected_symbol_1 == "AMZN":
        selected_symbol_1 = "Amazon"
    if selected_symbol_1 == "META":
        selected_symbol_1 = "Meta"
    if selected_symbol_2 == "AAPL":
        selected_symbol_2 = "Apple"
    if selected_symbol_2 == "MSFT":
        selected_symbol_2 = "Microsoft"
    if selected_symbol_2 == "ZM":
        selected_symbol_2 = "Zoom"
    if selected_symbol_2 == "AMZN":
        selected_symbol_2 = "Amazon"
    if selected_symbol_2 == "META":
        selected_symbol_2 = "Meta"
    st.write(f"The correlation between {selected_symbol_1} and {selected_symbol_2} Closing Price is : {correlation}")

    if (correlation <= 0.5 and correlation >=-0.5):
        st.write("Investing in these two companies could be interesting because if one company is in decline, the other is not affected.")
    else:
        st.write("These companies are too correlated, which makes them less interesting for portfolio diversification.")
    st.write("In our study, we only focus on NASDAQ tech stocks. However, if an investor wants to diversify their portfolio, they should consider changing sectors entirely.")

diversification()

# 5th insight

def crisis():
    spark_df = pd.read_csv("data/final/after_crisis.csv")
    spark_df['Date'] = pd.to_datetime(spark_df['Date'])
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("### Identifying the Most Resilient Stocks During a Crisis")
    st.write("In this insight, we will analyze how different companies performed during the 2022 crisis triggered by the war in Ukraine. Our focus will be on identifying the companies that experienced the least decline, highlighting those that demonstrated resilience during a period of global uncertainty. This analysis aims to help investors pinpoint stocks that are more stable in times of crisis.")

    fig = go.Figure()

    for symbol in SYMBOLS:
        column_name = f"Close_{symbol}"
        if column_name in spark_df.columns:
            fig.add_trace(go.Scatter(
                x=spark_df['Date'],
                y=spark_df[column_name],
                mode='lines', 
                name=symbol,  
                line=dict(width=2) 
            ))

    # layout
    fig.update_layout(
        title="Closing Price evolution after the crisis",
        xaxis_title="Years",
        yaxis_title="Closing Price",
        template='plotly_white',
        legend=dict(
            title="Legend",
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.2
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    close_columns = [col for col in spark_df.columns if col.startswith('Close_')]

    # Calculer la différence en pourcentage pour chaque colonne
    percentage_changes = {}
    for col in close_columns:
        first_value = spark_df[col].iloc[0]  # First
        last_value = spark_df[col].iloc[-1]  # Last
        percentage_change = ((last_value - first_value) / first_value) * 100
        percentage_changes[col] = percentage_change
    
    # Display percentage changes as sentences
    st.write("Here is the evolution of the closing prices for each stock since the crisis:")

    for col, change in percentage_changes.items():
        symbol = col.split('_')[1]  # Extract the stock symbol
        if change > 0:
            st.write(f"The closing price change for {symbol} is **{change:.2f}%**. This indicates an increase in price.")
        elif change < 0:
            st.write(f"The closing price change for {symbol} is **{change:.2f}%**. This indicates a decrease in price.")
        else:
            st.write(f"The closing price change for {symbol} is **0%**. The price has remained stable.")

    st.write("Analysis of Stock Price Movements After the Crisis:")
    st.write("This data suggests that Apple and Microsoft have been more resilient during the crisis, experiencing less of a drop in their stock prices compared to other major tech companies like Meta and Zoom. Investors may find these two stocks less volatile and potentially more stable options during periods of economic uncertainty.")

crisis()

# 6th insight

def scalability():
    #loading the file
    pandas = pd.read_csv("data/intermediate/cleaned_df.csv")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("### Understanding Stock Volatility")
    st.write("In this insight, we will analyze stock volatility, which refers to the variation in prices over time. By observing volatility, we can better understand the risks associated with each stock and adjust our investment strategy based on the fluctuations observed.")
    st.write("Next, we'll select a month to analyze which company has the highest volatility during that period.")

    pandas['Date'] = pd.to_datetime(pandas['Date'])
    pandas = pandas[pandas['Date'].dt.year >= 2020]

    # Extract the month and year to create a new column Month_Year
    pandas['Month_Year'] = pandas['Date'].dt.to_period('M')
    
    selected_month = st.selectbox(
        'Select a month', 
        pandas['Month_Year'].unique()
    )
    
    # Filter the data for the selcted month
    filtered_df = pandas[pandas['Month_Year'] == selected_month]
    
    volatility_columns = [col for col in filtered_df.columns if col.startswith('High_')]

    volatility = {}
    for col in volatility_columns:
        symbol = col.split('_')[1] 
        high_col = f'High_{symbol}'
        low_col = f'Low_{symbol}'

        volatility[symbol] = (filtered_df[high_col] - filtered_df[low_col]).mean()

    st.write(
        "The volatility for each stock is calculated as the difference between the highest and lowest prices within the selected month. "
        "Higher values indicate greater price fluctuations, while lower values suggest more stability."
    )

    
    volatility_df = pd.DataFrame(list(volatility.items()), columns=["Stock", "Volatility"])

    fig = px.bar(volatility_df, 
                 x="Stock", 
                 y="Volatility", 
                 title="Volatility of Stocks (High - Low) for the Selected Month", 
                 labels={"Volatility": "Volatility (High - Low)"}, 
                 color="Stock")

    st.plotly_chart(fig, use_container_width=True)
    for symbol, vol in volatility.items():
        if symbol == "AAPL":
            symbol = "Apple"
        if symbol == "MSFT":
            symbol = "Microsoft"
        if symbol == "AMZN":
            symbol = "Amazon"
        if symbol == "META":
            symbol = "Meta"
        if symbol == "ZM":
            symbol = "Zoom"
        st.write(f"For {symbol}, the average volatility in the selected month was **{vol:.2f}**.")
    st.write("After selecting several months, we observe that META is highly volatile, which can represent significant risks for investors but also large potential gains if managed well. On the other hand, companies like Apple and Microsoft are more stable, leading to lower risk.")

scalability()

# 7th insight

def prefered_month():
    panda = pd.read_csv("data/final/monthly_change.csv")

    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("### Identifying the Best and Worst Months for Investment")
    st.write("In this insight, we analyze the average monthly changes in stock prices to determine which months are best for investing and which should be avoided.")

    # Select only the columns containing the monthly changes.
    change_columns = [col for col in panda.columns if col.startswith("Monthly_Change")]

    #Calcule the mean value    
    pf = panda.groupby(['Month'])[change_columns].mean().reset_index()
    st.write("\n")
    colors = ['#ffaa0088', '#ff550088', '#0088ffaa', '#00ff5588', '#ff0088aa']
    st.write("**Average Monthly Changes in Stock Prices by Month**")

    st.bar_chart(pf, x="Month", y= change_columns, color= colors, stack=False)
    st.write("Based on the graphical analysis of the monthly changes, it is clear that March, September, and October generally show negative changes compared to the previous months. Investors may want to avoid investing during these months, as they tend to experience declines. On the other hand, February, April, July, and August often show positive monthly changes, indicating these months may offer better opportunities for investment.")

prefered_month()

# 8th insight

def plot_bollinger_bands():
    panda_mv = pd.read_csv("data/final/mv_avg_20.csv")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("### How Bollinger Bands Can Signal Market Opportunities")
    st.write("In this insight, we will explore Bollinger Bands, a popular technical analysis tool used to measure the volatility of a stock. Bollinger Bands consist of three lines: the simple moving average (SMA) in the center, the upper band, and the lower band. The upper and lower bands are typically set two standard deviations away from the SMA, and they adjust based on the stock's volatility.")
    panda_mv['Date'] = pd.to_datetime(panda_mv['Date'])
    panda_mv.set_index('Date', inplace=True)
    start_date = '2024-01-01'
    end_date = '2025-01-01'

    selection = st.radio(
        label="Select a Company to Visualize the Stock Trend :",
        options=SYMBOLS,
        key="radio_4"  # We have to use a unique because I am gonna use several radio widget
    )
    # Filtrer les données entre start_date et end_date
    panda_mv = panda_mv.loc[(panda_mv.index >= pd.to_datetime(start_date)) & (panda_mv.index <= pd.to_datetime(end_date))]

    panda_mv["Upper_Band"]=panda_mv[f"Close_{selection}_Moving_Avg_20"] + 2 * panda_mv[f"Close_{selection}"].rolling(window=20).std()
    panda_mv["Lower_Band"]=panda_mv[f"Close_{selection}_Moving_Avg_20"] - 2 * panda_mv[f"Close_{selection}"].rolling(window=20).std()

    # Créer la figure avec Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(panda_mv[f'Close_{selection}'], label='Closing Price', color='blue', alpha=0.6)
    ax.plot(panda_mv[f'Close_{selection}_Moving_Avg_20'], label='MA 20 days', color='red')
    ax.plot(panda_mv[f'Upper_Band'], label='Upper Band', color='green', linestyle='--')
    ax.plot(panda_mv[f'Lower_Band'], label='Lower Band', color='green', linestyle='--')

    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()

    st.write("**Bollinger Bands**")

    st.pyplot(fig)

    if selection == "AAPL":
        st.write("The Bollinger Bands show high volatility since mid-2024, with a strong upward trend from September 2024. The price is near the upper band, indicating buying pressure but also a risk of overbought conditions. A band contraction in early 2024 was followed by a sharp rally, suggesting similar patterns could signal future opportunities.")
        st.write("**Investor Tips :**")
        st.write("- The trend is strong, but being close to the upper band may indicate a possible correction.")
        st.write("- Watch for band contractions or a move back to the moving average to spot good entry or exit points.")
    if selection == "MSFT":
        st.write("The Bollinger Bands show several cycles of volatility in 2024, with periods of contraction followed by sharp expansions. A notable rally occurred until July 2024, when prices hit the upper band before a correction. Since September 2024, the stock shows signs of recovery, staying near the moving average and recently trending upward.")
        st.write("**Investor Tips :**")
        st.write("- Cyclical volatility requires close monitoring of band contractions, which may signal future opportunities.")
        st.write("- A close near the upper band could indicate a continued upward trend, though the risk of a correction remains.")
    if selection == "AMZN":
        st.write("The Bollinger Bands show a gradual price increase in 2024, with consolidation phases around the moving average and sharp expansions later in the year. Volatility rose from September 2024, accompanied by an upward trend, with prices often near or above the upper band, reflecting strong buying pressure.")
        st.write("**Investor Tips :**")
        st.write("- The upward trend is strong, but prices near the upper band suggest a potential overbought condition.")
        st.write("- A band contraction could signal an upcoming consolidation, offering potential entry points.")
    if selection == "META":
        st.write("Throughout the year, META's price frequently hovered around the 20-day moving average, suggesting periods of market indecision and consolidation.")
        st.write("Starting mid-year, there were clear expansions of the Bollinger Bands, coinciding with significant price moves. These reflect increased market volatility, potentially driven by news or broader market trends.")
        st.write("**Investor Tips :**")
        st.write("- The sustained upward trend suggests the potential for further growth. However, the proximity to the upper band in recent months could indicate short-term overbought conditions.")
        st.write("-  Increased volatility, particularly during the latter half of the year, offers trading opportunities for both momentum and mean-reversion strategies.")
    if selection == "ZM":
        st.write("The Bollinger Bands show a significant decline in the first half of 2024, followed by a sharp recovery starting mid-year. During the latter half, prices moved steadily upward, with periods of consolidation around the moving average and subsequent expansions. Volatility spiked in late 2024, as prices frequently tested the upper band, reflecting strong upward momentum.")
        st.write("**Investor Tips :**")
        st.write("- The sharp upward trend after mid-2024 signals a strong recovery phase. However, frequent testing of the upper band may indicate a potential overbought condition.")
        st.write("- Rising volatility toward the end of the year might signal further opportunities for breakout trades or trend continuations.")
    st.write("When the stock price touches or exceeds the upper band, it often precedes a price decline or consolidation, suggesting overbought conditions."
            "Conversely, when the price approaches or dips below the lower band, it often signals oversold conditions, leading to a potential rebound or upward movement.")

plot_bollinger_bands()

st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("A good understanding of stock trends and data visualization is crucial for making informed investment decisions. Throughout this analysis, we observed that Apple is a strong long-term investment, with consistent growth and resilience, making it a favorable option for investors looking for stability over time.")
st.write("Understanding phenomena like the Golden Cross and Death Cross can be extremely useful in identifying potential buying or selling opportunities, as these patterns signal important shifts in market trends. Recognizing these signals can help investors make timely decisions, optimizing their returns.")
st.write("Diversification is also a key strategy, especially during times of crisis. By holding a mix of assets, investors can protect their portfolios from significant losses in case one company underperforms, ensuring better overall stability.")
st.write("For those interested in short-term investments, analyzing volatility and knowing which months typically offer better performance can be advantageous. Utilizing tools like Bollinger Bands can further help by indicating potential overbought or oversold conditions, guiding investors on when to enter or exit the market.")
st.write("Ultimately, a combination of long-term strategies, a well-diversified portfolio, and short-term market analysis can provide a balanced approach to navigating the complexities of investing in the stock market.")