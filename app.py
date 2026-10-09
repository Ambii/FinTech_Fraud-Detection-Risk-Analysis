import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
import streamlit as st

# Load API key and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Page Header
st.title("Fraud Detection & Risk Analysis Dashboard")

# 1. Load Data
df = pd.read_csv("fintech_fraud_transactions.csv")

with st.sidebar:
    st.header("⚙️ Configuration")
    gemini_key = st.text_input(
        "Gemini API Key",
        value="",
        placeholder="Paste your Gemini API key here...",
        type="password",
        help="Paste your Google AI Studio API key here",
    )
    
    st.subheader("📁 Data Ingestion")
    uploaded_file = st.file_uploader(
        "Upload Custom Transactions (.csv)", type=["csv"]
    )
    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)
        st.success(f"Loaded: `{uploaded_file.name}`")

    st.divider()
    spike_multiplier = st.slider(
        "Spend Spike Threshold",
        min_value=2.0,
        max_value=10.0,
        value=3.5,
        step=0.5,
        help="Flags transactions exceeding X times the user's historical average.",
    )
    st.caption("10Pearls WTQ 2026 | FinTech Risk Track")

# 2. Compute Pandas Statistics (User baseline & spike ratio)
df["Avg_Spend"] = df.groupby("User_ID")["Amount"].transform("mean")
df["Spike_Ratio"] = df["Amount"] / df["Avg_Spend"]

# 3. Filter Suspicious Transactions
flagged_df = df[(df["Flagged_Status"] == 1) | (df["Spike_Ratio"] >= 3.0)]

# Display Tables
st.subheader("📋 Transaction Ledger & Filter")

view_option = st.radio(
    "Filter Log:",
    [
        "Flagged / High Risk Only",
        "Full Transaction Log",
        "Account Age < 30 Days",
    ],
    horizontal=True,
)

if view_option == "Flagged / High Risk Only":
    display_table = flagged_df
elif view_option == "Account Age < 30 Days":
    display_table = df[df["Account_Age_Days"] < 30]
else:
    display_table = df

st.dataframe(display_table[
        [
            "Transaction_ID",
            "User_ID",
            "Amount",
            "Avg_Spend",
            "Spike_Ratio",
            "Flagged_Status",
            "Merchant_Category",
            "Location",
            "Account_Age_Days"
        ]
    ].style.highlight_max(subset=["Spike_Ratio"], color="#ffcdd2"),
    use_container_width=True,
)

st.divider()


# 4. Select Transaction for AI Analysis
selected_id = st.selectbox(
    "Select Transaction to Investigate:", flagged_df["Transaction_ID"]
)
row = df[df["Transaction_ID"] == selected_id].iloc[0]

# Display Selected Details
st.write(
    f"**User:** {row['User_ID']} | **Amount:** ${row['Amount']:.2f} | **Avg:** ${row['Avg_Spend']:.2f} | **Spike:** {row['Spike_Ratio']:.1f}x"
)

# 5. Generate AI Risk Report
if st.button("Generate Risk Report"):
    if not gemini_key.strip():
        st.error("⚠️ Please enter a valid Gemini API Key in the sidebar first.")
    else:
        try:
            prompt = f"""
            Analyze this financial transaction for potential fraud:
            - Transaction ID: {row['Transaction_ID']}
            - User ID: {row['User_ID']}
            - Amount: ${row['Amount']:.2f}
            - Historical Average Spend: ${row['Avg_Spend']:.2f}
            - Spend Spike Ratio: {row['Spike_Ratio']:.1f}x
            - Merchant Category: {row['Merchant_Category']}
            - Location: {row['Location']}
            - Account Age: {row['Account_Age_Days']} days
        
            Explain why this is suspicious and state whether to FREEZE or APPROVE the account.
            """
            model = genai.GenerativeModel("gemini-3.5-flash-lite")
            response = model.generate_content(prompt)
            st.write(response.text)
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            