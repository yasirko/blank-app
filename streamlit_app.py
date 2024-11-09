import streamlit as st
import yfinance as yf
import pandas as pd

def check_tickers(tickers, percentage):
    results = {}
    multiplier = 1 + (percentage / 100)  # Convert percentage to a multiplier
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            
            if hist.empty:
                continue
            
            # Get the lowest 52-week price
            lowest_price = hist['Low'].min()
            current_price = hist['Close'].iloc[-1]
            
            # Check if current price is between lowest price and lowest price * multiplier
            if lowest_price <= current_price <= lowest_price * multiplier:
                results[ticker] = {
                    'current_price': round(current_price, 2),
                    'lowest_52_week_price': round(lowest_price, 2)
                }
        except Exception as e:
            st.error(f"Error processing {ticker}: {str(e)}")
    
    return results

# Streamlit app
st.title("Stock Price Checker")

# Input for tickers
default_tickers = ', '.join([
    '1010.SR', '1020.SR', '1030.SR', '1050.SR', '1060.SR', '1080.SR', 
    # ... (rest of the tickers)
    '8310.SR', '8311.SR'
])
tickers_input = st.text_area("Enter stock tickers (comma-separated)", value=default_tickers)
tickers_to_check = [ticker.strip() for ticker in tickers_input.split(',')]

# Input for percentage
percentage_input = st.number_input("Enter the percentage for upper limit", 
                                    min_value=0.0, 
                                    max_value=100.0, 
                                    value=10.0,
                                    step=0.1)

# Button to check prices
if st.button("Check Prices"):
    with st.spinner("Checking prices..."):
        result = check_tickers(tickers_to_check, percentage_input)
    
    # Display results
    if result:
        st.success("Stocks within the price range:")
        df = pd.DataFrame.from_dict(result, orient='index')
        st.dataframe(df)
    else:
        st.warning("No stocks found within the specified price range.")
