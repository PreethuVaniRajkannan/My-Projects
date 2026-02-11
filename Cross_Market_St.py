import streamlit as st
import pandas as pd
import pymysql


#connection to mysql
conn = pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    password = "tatsavi",
)
cursor = conn.cursor()
#calling database
cursor.execute("Use market_data")


#Navigaton bar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ["DASHBOARD", "SQL QUERY TABLE", "Crypto Analysis"]
)
if page == "DASHBOARD":
    st.set_page_config(page_title="DASHBOARD", page_icon="📊",layout="wide")
    st.title(":red[CROSS MARKET ANALYSIS DASHBOARD]")
    st.caption("Crypto • Stocks • Oil ")
    st.divider()
    
    
    #SQL query for average price trends
    #GET DATE RANGE
    dateq = """
    SELECT DISTINCT date
    FROM crypto_prices2
    ORDER BY date;
    """
    cursor.execute(dateq)
    dateq = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
    dates = dateq["date"].tolist()
    
    #DATE dropdowns
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.selectbox(
        "Select Start Date",
        dates,
        index=0
        )
    with col2:
        end_date = st.selectbox(
        "Select End Date",
        dates,
        index=len(dates) - 1
        )
    
    if start_date > end_date:
        st.error("❌ Start date must be before End date")
        st.stop()
    
    #average prices sql query
    average = """
    SELECT
        cp.date,
        cp.prices AS Bitcoin_Price,
        op.price AS Oil_Price,
        sp1.Close AS SP500_Price,
        sp2.Close AS NIFTY_Price
    FROM crypto_prices2 cp
    JOIN oil_prices3 op
        ON cp.date = op.Date
    JOIN stock_prices4 sp1
        ON cp.date = sp1.Date AND sp1.Tickers = '^GSPC'
    JOIN stock_prices4 sp2
        ON cp.date = sp2.Date AND sp2.Tickers = '^NSEI'
    WHERE cp.coin_id = 'bitcoin'
    ORDER BY cp.date DESC
    LIMIT 1;
    """
    cursor.execute(average, {"start": start_date, "end": end_date})
    average = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
    
    date = average.loc[0, "date"]
    btc =average.loc[0, "Bitcoin_Price"]
    oil = average.loc[0, "Oil_Price"]
    sp500 = average.loc[0, "SP500_Price"]
    nifty = average.loc[0, "NIFTY_Price"]
    st.subheader("Average Prices")
    
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric("₿ Bitcoin Avg ($)", f"{btc:,.2f}")
    c2.metric("🛢 Oil Avg ($)", f"{oil:,.2f}")
    c3.metric("📈 S&P 500 Avg", f"{sp500:,.2f}")
    c4.metric("🇮🇳 NIFTY Avg", f"{nifty:,.2f}")
    
    st.divider()
    #SQL query for market trends
    market_display = """
    SELECT
        cp.date AS Date,
        cp.prices AS Bitcoin_Price,
        op.price AS Oil_Price,
        sp1.Close AS SP500_Price,
        sp2.Close AS NIFTY_Price
    FROM crypto_prices2 cp
    INNER JOIN oil_prices3 op
        ON cp.date = op.Date
    INNER JOIN stock_prices4 sp1
        ON cp.date = sp1.Date AND sp1.Tickers = '^GSPC'
    INNER JOIN stock_prices4 sp2
        ON cp.date = sp2.Date AND sp2.Tickers = '^NSEI'
    WHERE cp.coin_id = 'bitcoin'
    ORDER BY cp.date DESC;
    """
    # Load data
    cursor.execute(market_display)
    market_display = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
    
    #Display table
    st.subheader("📅 Daily Prices (Combined View)")
    st.dataframe(
        market_display,
        use_container_width=True
    )
    
    st.divider()
#page2
if page == "SQL QUERY TABLE":
    st.set_page_config(page_title="SQL QUERY TABLE", page_icon="📈",layout="wide")
    st.title("📊 :red[QUERY TABLES]")
    #query selection box
    option = st.selectbox(
        "Please select the query from the drop down",
    #options to queries
        ("1. Top 3 Cryptocurrencies by market cap",
        "2. Circulating supply exceeds 90% of total supply",
        "3. Get coins that are within 10% of their all-time-high (ATH)",
        "4. Find the average market cap rank of coins with volume above $1B",
        "5. Get the most recently updated coin",
        "6. Find the highest daily price of Bitcoin in the last 365 days",
        "7. Calculate the average daily price of Ethereum in the past 1 year",
        "8. Show the daily price trend of Bitcoin in March 2025",
        "9. Find the coin with the highest average price over 1 year",
        "10. Get the % change in Bitcoin’s price between Mar 2025 and Sep 2025",
        "11. Find the highest oil price in the last 5 years",
        "12. Get the average oil price per year",
        "13. Show oil prices during COVID crash (March–April 2020)",
        "14. Find the lowest price of oil in the last 10 years",
        "15. Calculate the volatility of oil prices (max-min difference per year",
        "16. Get all stock prices for a given ticker",
        "17. Find the highest closing price for NASDAQ (^IXIC)",
        "18. List top 5 days with highest price difference (high - low) for S&P 500 (^GSPC)",
        "19. Get monthly average closing price for each ticker",
        "20. Get average trading volume of NSEI in 2024",
        "21. Compare Bitcoin vs Oil average price in 2025",
        "22. Check if Bitcoin moves with S&P 500 (correlation idea)",
        "23. Compare Ethereum and NASDAQ daily prices for 2025",
        "24. Find days when oil price spiked and compare with Bitcoin price change",
        "25. Compare top 3 coins daily price trend vs Nifty (^NSEI)",
        "26. Compare stock prices (^GSPC) with crude oil prices on the same dates",
        "27. Correlate Bitcoin closing price with crude oil closing price (same date)",
        "28. Compare NASDAQ (^IXIC) with Ethereum price trends",
        "29. Join top 3 crypto coins with stock indices for 2025",
        "30. Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison")
        )
    #options results - SQL queries
    st.write("You Selected:", option)
    corr = None   #--------if correlation not available
    
    if option == "1. Top 3 Cryptocurrencies by market cap" :
        cursor.execute ("""SELECT id, symbol, name, market_cap 
    FROM crypto_currencies1
    ORDER BY market_cap DESC
    LIMIT 3; """)
        qdf1 = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf1)
    
    if option == "2. Circulating supply exceeds 90% of total supply" :
        cursor.execute ("""
        SELECT 
        id,
        symbol,
        name,
        current_price,
        ath,
        (current_price/ath) *100 as p_ath
    FROM crypto_currencies1 where ath IS NOT NULL
        AND ath > 0
        AND current_price >= 0.9 * ath
    order by p_ath;""")
        qdf2 = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf2)
        
    if option == "3. Get coins that are within 10% of their all-time-high (ATH)" :
        cursor.execute("""
        SELECT 
        id,
        symbol,
        name,
        current_price,
        ath,
        (current_price/ath) *100 as p_ath
    FROM crypto_currencies1 where ath IS NOT NULL
        AND ath > 0
        AND current_price >= 0.9 * ath
    order by p_ath;
    """)
        qdf3 = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf3)
    
    if option == "4. Find the average market cap rank of coins with volume above $1B":
        cursor.execute("""
        Select avg(market_cap_rank)
    from crypto_currencies1
    where total_volume > 1000000000
    """ )
        qdf4 = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf4)
    
    if option == "5. Get the most recently updated coin":
        cursor.execute("""
         select * from crypto_currencies1
    order by last_updated desc
    limit 1;""")
        qdf5 = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf5)
    
    if option == "6. Find the highest daily price of Bitcoin in the last 365 days":
        cursor.execute("""
         Select max(prices) from crypto_prices2 where coin_id = "bitcoin" ;
         """)
        qdf6 = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf6)
    
    if option == "7. Calculate the average daily price of Ethereum in the past 1 year":
        cursor.execute("""
        Select avg(prices) from crypto_prices2 where coin_id = "ethereum";
        """)
        qdf7 = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf7)
    
    
    if option == "8. Show the daily price trend of Bitcoin in March 2025":
        cursor.execute("""
    Select * from crypto_prices2 where coin_id = "bitcoin"
    and date between '2025-03-01' AND '2025-03-31'
    order by date;
    """)
        qdf8 = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf8)
    
    if option == "9. Find the coin with the highest average price over 1 year":
        cursor.execute("""
        Select coin_id,  (avg(prices)) as average_price 
    from crypto_prices2
    group by coin_id
    order by average_price desc
    limit 1;""")
        qdf9 = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf9)
        
    if option == "10. Get the % change in Bitcoin’s price between Mar 2025 and Sep 2025":
        cursor.execute("""
        SELECT
        ROUND(
            (p2.prices - p1.prices) / p1.prices * 100, 2) AS pct_change
    FROM
        (SELECT prices FROM crypto_prices2
         WHERE coin_id='bitcoin' AND date='2025-03-30') p1,
        (SELECT prices FROM crypto_prices2
         WHERE coin_id='bitcoin' AND date='2025-09-30') p2;
    """)
        qdf10 = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf10)
        
    if option == "11. Find the highest oil price in the last 5 years":
        cursor.execute("""
        Select max(Price) from oil_prices3 ;
        """)
        qdf11 = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf11)
    
    if option == "12. Get the average oil price per year":
        cursor.execute("""
        Select 
    YEAR(Date) as Year,
    avg(Price) as Avg
    from oil_prices3 
    Group by YEAR(Date)
    order by year ;
        """)
        qdf12= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf12)
    
    if option == "13. Show oil prices during COVID crash (March–April 2020)":
        cursor.execute("""
        Select *
        from oil_prices3 
        where Date between '2020-03-01' AND '2020-04-30'
        order by Price, Date;""")
        qdf13= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf13)
    
    if option == "14. Find the lowest price of oil in the last 10 years":
        cursor.execute("""
        Select min(Price)
        from oil_prices3; 
        """)
        qdf14= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf14)
    
    if option == "15. Calculate the volatility of oil prices (max-min difference per year":
        cursor.execute("""
        Select
        YEAR(Date) AS year,
        STDDEV(Price) AS Volatality_per_year
    FROM oil_prices3
    GROUP BY YEAR(Date)
    ORDER BY year;
    """)
        qdf15= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf15) 
    
    if option == "16. Get all stock prices for a given ticker":
        cursor.execute("""
    SELECT *
    FROM stock_prices4
    WHERE Tickers = '^NSEI';
    """)
        qdf16= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf16) 
    
    if option == "17. Find the highest closing price for NASDAQ (^IXIC)":
        cursor.execute("""
        SELECT MAX(Close)
        FROM stock_prices4
        WHERE Tickers = '^IXIC'
        """)
        qdf17= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf17)
    
    if option == "18. List top 5 days with highest price difference (high - low) for S&P 500 (^GSPC)":
        cursor.execute("""
        SELECT
            date,
            high,
            low,
            (high - low) AS price_difference
        FROM stock_prices4
        WHERE Tickers = '^GSPC'
        ORDER BY price_difference DESC
        LIMIT 5;
        """ )
        qdf18= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf18)
    
    if option == "19. Get monthly average closing price for each ticker":
        cursor.execute("""
        SELECT 
        Tickers,
        MONTH(Date) AS Months, 
        AVG(Close) AS Average
        
        FROM stock_prices4
        GROUP BY Tickers, Month(Date)
        Order By Tickers, Months;
        """)
        qdf19= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf19)
    
    if option =="20. Get average trading volume of NSEI in 2024":
        cursor.execute("""
            Select 
        Tickers,
        year(Date) AS Year,
        avg(Volume) AS Trading_Volume_Avg
        from stock_prices4
        where year(Date) = "2024" AND Tickers = "^NSEI"
        group by year(Date)
        """)
        qdf20= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf20)
    
    if option == "21. Compare Bitcoin vs Oil average price in 2025":
        cursor.execute("""
        Select 
    ( SELECT AVG(prices) 
    FROM crypto_prices2
    WHERE coin_id = 'bitcoin'
    AND date BETWEEN '2025-01-01' AND '2025-12-31') As Bitcoin_AVG_Price,
    
    (SELECT AVG(Price)
    FROM oil_prices3
    WHERE Date BETWEEN '2025-01-01' AND '2025-12-31') AS Oil_AVG_Price;
    """)
        qdf21= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf21)
        
    if option == "22. Check if Bitcoin moves with S&P 500 (correlation idea)":
        cursor.execute("""
        SELECT
        cp.date,
        cp.coin_id,
        cp.prices AS Bitcoin_Price,
        sp.Close as SP500_Price
    FROM crypto_prices2 cp
    INNER JOIN stock_prices4 sp 
        ON cp.date = sp.Date 
    WHERE cp.coin_ID = "bitcoin"
    AND sp.Tickers = '^GSPC'
    ORDER BY cp.date;
    """)
        qdf22= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf22)
        corr = qdf22['Bitcoin_Price'].corr(qdf22['SP500_Price'])
        
        
    if option == "23. Compare Ethereum and NASDAQ daily prices for 2025":
        cursor.execute("""
        SELECT
        c.date AS date,
        c.prices AS ethereum_price,
        s.Close AS nasdaq_price
    FROM crypto_prices2 c
    JOIN stock_prices4 s
      ON c.date = s.Date
    WHERE c.coin_id = 'ethereum'
      AND s.Tickers = '^IXIC'
      AND c.date BETWEEN '2025-01-01' AND '2025-12-31'
    ORDER BY date;
    """)
        qdf23= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf23) 
    
    if option == "24. Find days when oil price spiked and compare with Bitcoin price change":
        cursor.execute("""
        SELECT
        o1.Date,
        -- Oil prices
        o1.Price AS oil_price_today,
        o2.Price AS oil_price_yesterday,
        (o1.Price - o2.Price) AS oil_price_change,
    
        -- Bitcoin prices
        b1.prices AS bitcoin_price_today,
        b2.prices AS bitcoin_price_yesterday,
        (b1.prices - b2.prices) AS bitcoin_price_change
    
    FROM oil_prices3 o1
    INNER JOIN oil_prices3 o2
        ON o1.Date = DATE_ADD(o2.Date, INTERVAL 1 DAY)
    
    INNER JOIN crypto_prices2 b1
        ON o1.Date = b1.date AND b1.coin_id = 'bitcoin'
    INNER JOIN crypto_prices2 b2
        ON o2.Date = b2.date AND b2.coin_id = 'bitcoin'
    
    WHERE o1.Price > o2.Price
    ORDER BY o1.Date;
    """)
        qdf24= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf24) 
    
    if option == "25. Compare top 3 coins daily price trend vs Nifty (^NSEI)":
        cursor.execute("""
        SELECT
        cp.date,
        cp.coin_id,
        cp.prices AS crypto_price,
        sp.Close AS nifty_price
    FROM crypto_prices2 cp
    
    INNER JOIN stock_prices4 sp
        ON cp.date = sp.date
        AND sp.Tickers = '^NSEI'
    
    INNER JOIN (
        SELECT id
        FROM crypto_currencies1
        ORDER BY market_cap DESC
        LIMIT 3
    ) top3
        ON cp.coin_id = top3.id
    
    ORDER BY cp.date, cp.coin_id;
    """)
        qdf25= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf25) 
    
    if option == "26. Compare stock prices (^GSPC) with crude oil prices on the same dates":
        cursor.execute("""
        SELECT
        sp.date,
        sp.Close AS GSPC_prices,
        op.Price as Crude_oil_Price
    FROM stock_prices4 sp
    INNER JOIN oil_prices3 op 
        ON sp.date = op.Date 
    WHERE sp.Tickers = "^GSPC"
    ORDER BY sp.date;
    """)
        qdf26= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf26) 
    
    if option == "27. Correlate Bitcoin closing price with crude oil closing price (same date)":
        cursor.execute("""
        SELECT
        cp.date,
        cp.coin_id,
        cp.prices AS bitcoin_price,
        op.Price as Crude_oil_Price
    FROM crypto_prices2 cp
    INNER JOIN oil_prices3 op 
        ON cp.date = op.Date 
    WHERE cp.coin_ID = "bitcoin"
    ORDER BY cp.date;
    """)
        qdf27= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf27)
        corr = qdf27['bitcoin_price'].corr(qdf27['Crude_oil_Price'])
    
    if option == "28. Compare NASDAQ (^IXIC) with Ethereum price trends":
        cursor.execute("""
        SELECT
        cp.date,
        cp.prices AS ethereum_price,
        sp.Close AS nasdaq_price
    FROM crypto_prices2 cp
    INNER JOIN stock_prices4 sp
      ON cp.date = sp.Date
    WHERE cp.coin_id = 'ethereum'
      AND sp.Tickers = '^IXIC'
    ORDER BY cp.date;
    """)
        qdf28= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf28)
        corr = qdf28['ethereum_price'].corr(qdf28['nasdaq_price'])
    
    if option == "29. Join top 3 crypto coins with stock indices for 2025":
        cursor.execute("""
        SELECT 
        cp.date,
        cp.coin_id,
        cp.prices AS crypto_price,
        sp.Tickers AS stock_index,
        sp.Close AS stock_close
    FROM crypto_prices2 cp
    INNER JOIN stock_prices4 sp
        ON cp.date = sp.Date 
    WHERE cp.coin_id IN ('bitcoin', 'ethereum', 'tether')
      AND sp.Tickers IN ('^GSPC', '^IXIC', '^NSEI')
      AND cp.date BETWEEN '2025-01-01' AND '2025-12-31'
    ORDER BY cp.date, cp.coin_id, sp.Tickers;
    """)
        qdf29= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf29)
    
    if option == "30. Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison":
        cursor.execute("""
        SELECT 
        cp.date,
        cp.prices AS Bitcoin_price,
        op.Price as Crude_oil_Price,
        sp.Tickers AS Stock_index,
        sp.Close AS stock_close
    
    FROM crypto_prices2 cp
    
    JOIN oil_prices3 op
        ON cp.date = op.Date 
    JOIN stock_prices4 sp
        ON cp.date = sp.Date 
    WHERE cp.coin_id = 'bitcoin'
      AND sp.Tickers IN ('^GSPC', '^IXIC', '^NSEI')
    ORDER BY cp.date, sp.Tickers;
    
    """)
        qdf30= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
        st.dataframe(qdf30)
    
    st.divider()
    
    st.button("Correlation value") 
    if corr is not None:
        st.metric("📊 Correlation", round(corr, 4))
    else:
        st.warning("⚠ Correlation not available for this query.")
    
#third page
if page == "Crypto Analysis":
    st.set_page_config(page_title="Crypto Analysis", page_icon="📈")
    st.title(":red[TOP 5 CRYPTO ANALYSIS]")
    st.divider()
    
    #Connection to coin ids for selection box
    cursor.execute( "SELECT DISTINCT coin_id FROM crypto_prices2 ORDER BY coin_id")
    coins = pd.DataFrame(cursor.fetchall(),columns=[c[0] for c in cursor.description])
    cc = st.selectbox(
        "Select a Crypto Currrency",
         coins["coin_id"],
         key="crypto_selectbox")  
    
    #date selection
    #Fetching data
    dateq = """
    SELECT DISTINCT date
    FROM crypto_prices2
    ORDER BY date;
    """
    cursor.execute(dateq)
    dateq = pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
    dates = dateq["date"].tolist()
    D1, D2 = st.columns(2)
    with D1:
        start_date = st.selectbox(
        "Select Start Date",
        dates,
        index=0,
        key='date_start'
        )
    with D2:
        end_date = st.selectbox(
        "Select End Date",
        dates,
        index=len(dates) - 1,
        key = "date_end"
        )
    
    if start_date > end_date:
        st.error("❌ Start date must be before End date")
        st.stop()
    
    #trend analysis
    st.header(":blue[TREND ANALYSIS]")
    st.divider()
    qdf1 = """
    SELECT DATE(`date`) AS date, prices
    FROM crypto_prices2
    WHERE coin_id = %s
    AND DATE(`date`) BETWEEN %s AND %s
    ORDER BY DATE(`date`)
    """
    cursor.execute(qdf1, (cc, start_date, end_date))  
    qdf1= pd.DataFrame(cursor.fetchall(), columns=[c[0] for c in cursor.description])
    if qdf1.empty:
        st.warning("No data available for selected range")
    else:
        st.line_chart(
            qdf1.set_index("date")["prices"],
            use_container_width=True
        )
    st.divider()
    st.header(":blue[DETAILED VIEW - TABLE]")
    st.dataframe(qdf1, use_container_width=True)
