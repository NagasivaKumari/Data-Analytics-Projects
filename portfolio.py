import streamlit as st
import pandas as pd
import plotly.express as px

# --- Sample Data (Synthetic - replace with your data loading) ---
data = {
    'Date': pd.to_datetime(['2023-01-01', '2023-01-08', '2023-01-15', '2023-01-22', '2023-01-29',
                           '2023-02-05', '2023-02-12', '2023-02-19', '2023-02-26', '2023-03-05']),
    'Portfolio Value': [10000, 10200, 10500, 10300, 10600, 10800, 11000, 10900, 11200, 11500],
    'Stock A': [100, 102, 105, 103, 106, 108, 110, 109, 112, 115],
    'Stock B': [200, 202, 205, 203, 206, 208, 210, 209, 212, 215],
    'Stock C': [50, 51, 52, 51, 53, 54, 55, 54, 56, 57]
}
df = pd.DataFrame(data)

# --- Streamlit App ---
st.title("Stock Portfolio Performance Dashboard")

st.subheader("Portfolio Value Over Time")
fig_portfolio = px.line(df, x="Date", y="Portfolio Value", title="")
st.plotly_chart(fig_portfolio)

st.subheader("Individual Stock Performance")
selected_stocks = st.multiselect("Select Stocks to View:",
                                 [col for col in df.columns if col not in ['Date', 'Portfolio Value']],
                                 default=['Stock A', 'Stock B'])
if selected_stocks:
    fig_stocks = px.line(df, x="Date", y=selected_stocks, title="")
    st.plotly_chart(fig_stocks)
else:
    st.write("Please select stocks to view individual performance.")


