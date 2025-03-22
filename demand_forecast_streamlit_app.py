import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error

# --- Synthetic Retail Sales Data ---
np.random.seed(42)
start_date = pd.to_datetime('2023-01-01')
dates = pd.date_range(start_date, periods=365, freq='D') # 365 days of data
product_categories = ['Electronics', 'Clothing', 'Home Goods', 'Books']

sales_data = []
for category in product_categories:
    # Simulate trend and seasonality (simplified)
    trend = np.linspace(50, 150, len(dates)) + (np.random.rand() * 20)  # Increasing trend + random offset
    seasonality = 50 * np.sin(np.linspace(0, 4 * np.pi, len(dates))) # Sine wave for seasonality
    base_sales = trend + seasonality + 200  # Base sales with trend and seasonality
    noise = np.random.normal(0, 30, len(dates)) # Add noise
    actual_sales = np.maximum(base_sales + noise, 0) # Ensure sales are not negative

    forecasted_sales = base_sales # Simplified forecast - using base trend+seasonality as "forecast" for example

    for i, date in enumerate(dates):
        sales_data.append({'Date': date, 'Product Category': category, 'Actual Sales': actual_sales[i], 'Forecasted Sales': forecasted_sales[i]})

df_sales = pd.DataFrame(sales_data)


# --- Calculate Forecast Accuracy Metrics ---
def calculate_forecast_metrics(df):
    actual = df['Actual Sales']
    forecast = df['Forecasted Sales']
    mape = mean_absolute_percentage_error(actual, forecast) * 100
    rmse = np.sqrt(mean_squared_error(actual, forecast))
    return mape, rmse

overall_mape, overall_rmse = calculate_forecast_metrics(df_sales)


# --- Streamlit App ---
st.title("Demand Forecasting & Inventory Optimization Dashboard")

# --- Page 1: Sales Trends and Forecasts ---
st.header("Sales Trends & Forecasts")

# --- Product Category Filter ---
selected_category = st.selectbox("Select Product Category:", ['All'] + list(product_categories))

if selected_category == 'All':
    filtered_sales_df = df_sales
else:
    filtered_sales_df = df_sales[df_sales['Product Category'] == selected_category]

# --- Historical Sales & Forecasted Sales Line Chart ---
st.subheader(f"Sales Performance for {selected_category if selected_category != 'All' else 'All Categories'}")
sales_chart_data = filtered_sales_df[['Date', 'Actual Sales', 'Forecasted Sales']]
sales_fig = px.line(sales_chart_data, x="Date", y=['Actual Sales', 'Forecasted Sales'],
                    title=f"Actual vs. Forecasted Sales - {selected_category if selected_category != 'All' else 'All Categories'}",
                    labels={'value': 'Sales Quantity', 'variable': 'Sales Type'}) # Improved legend label
st.plotly_chart(sales_fig)


# --- Forecast Accuracy Metrics (Cards) ---
if selected_category == 'All':
    mape_value = overall_mape
    rmse_value = overall_rmse
else:
    category_mape, category_rmse = calculate_forecast_metrics(filtered_sales_df)
    mape_value = category_mape
    rmse_value = category_rmse

st.subheader("Forecast Accuracy Metrics")
col1, col2 = st.columns(2) # Create two columns for metrics side-by-side
with col1:
    st.metric(label="Mean Absolute Percentage Error (MAPE)", value=f"{mape_value:.2f}%")
with col2:
    st.metric(label="Root Mean Squared Error (RMSE)", value=f"{rmse_value:.2f}")


st.subheader("Sales Trend Decomposition (Simplified Placeholder)")
st.write("Sales Trend Decomposition visualization (showing trend, seasonality, residuals) would be implemented here in a more advanced dashboard.  This is a placeholder for demonstration. Time series decomposition often requires libraries like `statsmodels` and more complex plotting. For now, the line chart above provides a visual overview of actual vs. forecast.")


# --- Page 2: Inventory Management (Simplified Placeholder) ---
st.header("Inventory Management (Simplified Placeholder)")
st.write("Inventory Management metrics and visualizations (like Inventory Levels, Days of Supply, Inventory Turnover, Stockout Rate) would be included on this page in a more complete dashboard.  This section is currently a placeholder to indicate where inventory analysis would be incorporated in a real-world application.  To develop this further, you would need to add data or simulations for inventory levels, reorder points, and potentially cost information.")
st.write("Further development would include: Time series decomposition visualization, more sophisticated forecasting models, inventory management metrics and visualizations, interactive time period selection, and potentially drill-down into store-level or regional sales data.")