import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Synthetic Credit Risk Data ---
np.random.seed(42)  # for reproducibility
n_samples = 1000
credit_scores = np.random.normal(loc=650, scale=80, size=n_samples)
income = np.random.uniform(low=30000, high=150000, size=n_samples)
loan_amount = np.random.uniform(low=5000, high=50000, size=n_samples)
dti_ratio = np.random.uniform(low=0.1, high=0.5, size=n_samples) # Debt-to-Income ratio
loan_purposes = np.random.choice(['Home Improvement', 'Car Loan', 'Personal Loan', 'Debt Consolidation'], size=n_samples)

# Simulate Default outcome - higher risk if score is lower, DTI is higher, loan amount higher
probability_default = 1 / (1 + np.exp(-(0.05 * credit_scores - 0.01 * income + 0.02 * loan_amount + 5 * dti_ratio - 3))) # Sigmoid-like function
default_outcome = np.random.binomial(1, probability_default) # 1 for default, 0 for no default

data = {
    'Credit Score': credit_scores,
    'Income': income,
    'Loan Amount': loan_amount,
    'Debt-to-Income Ratio': dti_ratio,
    'Loan Purpose': loan_purposes,
    'Defaulted': default_outcome
}
df_credit = pd.DataFrame(data)

# --- Streamlit App ---
st.title("Credit Risk Assessment Dashboard")

# --- Overall Default Rate ---
default_rate = df_credit['Defaulted'].mean() * 100
st.subheader("Overall Default Rate")
st.metric(label="Default Rate", value=f"{default_rate:.2f}%")

# --- Credit Score Distribution ---
st.subheader("Credit Score Distribution")
hist_fig = px.histogram(df_credit, x="Credit Score", nbins=30, title="Distribution of Applicant Credit Scores")
st.plotly_chart(hist_fig)

# --- Key Risk Factor Drivers (Example - simplified and synthetic) ---
st.subheader("Key Risk Factor Example (Synthetic)")
risk_factors = pd.DataFrame({
    'Risk Factor': ['Credit Score (Lower)', 'Debt-to-Income Ratio (Higher)', 'Loan Amount (Higher)'],
    'Impact on Risk': [ "Strong Negative", "Moderate Positive", "Slight Positive"] # Example qualitative impacts
})
st.table(risk_factors) # Or st.dataframe for interactive table

# --- Filter by Loan Purpose (Dropdown) ---
st.subheader("Filter by Loan Purpose")
selected_purpose = st.selectbox("Select Loan Purpose:", ['All'] + list(df_credit['Loan Purpose'].unique()))

if selected_purpose != 'All':
    filtered_df = df_credit[df_credit['Loan Purpose'] == selected_purpose]
    filtered_default_rate = filtered_df['Defaulted'].mean() * 100
    st.metric(label=f"Default Rate for {selected_purpose} Loans", value=f"{filtered_default_rate:.2f}%")

    filtered_hist_fig = px.histogram(filtered_df, x="Credit Score", nbins=30,
                                      title=f"Credit Score Distribution for {selected_purpose} Loans")
    st.plotly_chart(filtered_hist_fig)
else:
    st.info("Displaying overall metrics and distributions for all loan purposes. Use the dropdown to filter by a specific loan purpose.")