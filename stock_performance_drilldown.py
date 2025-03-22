import streamlit as st
import pandas as pd
import plotly.express as px

# --- Sample Data (Synthetic - Replace with your data loading) ---
data = {
    'Date': pd.to_datetime(['2023-01-01', '2023-01-08', '2023-01-15', '2023-01-22', '2023-01-29',
                           '2023-02-05', '2023-02-12', '2023-02-19', '2023-02-26', '2023-03-05']),
    'Stock A': [100, 102, 105, 103, 106, 108, 110, 109, 112, 115],
    'Stock B': [200, 202, 205, 203, 206, 208, 210, 209, 212, 215],
    'Stock C': [50, 51, 52, 51, 53, 54, 55, 54, 56, 57]
}
df = pd.DataFrame(data)

# Calculate Daily Returns (percentage change from previous day)
stocks = ['Stock A', 'Stock B', 'Stock C']
for stock in stocks:
    df[f'{stock} Daily Return'] = df[stock].pct_change() * 100

# --- Streamlit App ---
st.title("Stock Performance Drill-Down Dashboard")

st.subheader("Select Stocks for Detailed Analysis")
selected_stocks = st.multiselect("Choose Stocks:", stocks, default=stocks[:2]) # Default to first two stocks

if not selected_stocks:
    st.warning("Please select at least one stock to analyze.")
else:
    # --- Individual Stock Performance Line Chart ---
    st.subheader("Individual Stock Performance Over Time")
    price_chart_data = df[['Date'] + selected_stocks] # Select Date and chosen stock price columns
    price_fig = px.line(price_chart_data, x="Date", y=selected_stocks,
                          title=f"Stock Prices for: {', '.join(selected_stocks)}")
    st.plotly_chart(price_fig)

    # --- Daily Returns Bar Chart ---
    st.subheader("Daily Returns for Selected Stocks")
    returns_columns = [f'{stock} Daily Return' for stock in selected_stocks]
    returns_chart_data = df[['Date'] + returns_columns].dropna() # Remove NaN from pct_change first row
    returns_fig = px.bar(returns_chart_data, x="Date", y=returns_columns,
                         title=f"Daily Returns (%) for: {', '.join(selected_stocks)}")
    st.plotly_chart(returns_fig)

    # --- Stock Comparison Table ---
    st.subheader("Stock Comparison Metrics")
    comparison_data = []
    for stock in selected_stocks:
        latest_price = df[stock].iloc[-1]  # Last price in the dataset
        daily_return = df[f'{stock} Daily Return'].iloc[-1] # Last daily return
        # (For YTD and Volatility, you'd need more historical data or calculations) - placeholders for now
        ytd_return = "N/A (Example Data)"
        volatility = "N/A (Example Data)"

        comparison_data.append({
            "Stock": stock,
            "Current Price": latest_price,
            "Daily Return (%)": f"{daily_return:.2f}%", # Format to 2 decimal places with %
            "YTD Return": ytd_return,
            "Volatility": volatility
        })
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df) # Or st.table(comparison_df) for static table