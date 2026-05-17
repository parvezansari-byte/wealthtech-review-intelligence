import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Review Explorer",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📝 WealthTech Review Explorer")

st.markdown("""
Platform-wise review intelligence and categorization engine.
""")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

try:

    df = pd.read_csv(
        "data/historical_reviews.csv"
    )

except Exception as e:

    st.error(f"Data Load Error: {e}")

    st.stop()

# ---------------------------------------------------
# EMPTY CHECK
# ---------------------------------------------------

if df.empty:

    st.error("No review data found.")

    st.stop()

# ---------------------------------------------------
# CATEGORY ENGINE
# ---------------------------------------------------

def categorize_review(text):

    text = str(text).lower()

    if any(word in text for word in [
        "login",
        "otp",
        "signin",
        "password"
    ]):

        return "Login Issues"

    elif any(word in text for word in [
        "crash",
        "bug",
        "slow",
        "hang"
    ]):

        return "App Performance"

    elif any(word in text for word in [
        "kyc",
        "onboarding",
        "verification"
    ]):

        return "Onboarding/KYC"

)
