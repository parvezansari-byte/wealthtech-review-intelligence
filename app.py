import streamlit as st
import pandas as pd

from scraper.review_scraper import fetch_reviews
from analytics.sentiment import analyze_sentiment

st.set_page_config(
    page_title="WealthTech Review Intelligence Dashboard",
    layout="wide"
)

st.title("WealthTech Review Intelligence Dashboard")

apps = {
    "NJ Wealth": "com.nj.ewa",
    "FundsIndia": "com.fundsindia.consumer",
    "Nuvama": "com.msf.nuvama",
    "AssetPlus": "com.assetplus.app",
    "Wealthy": "in.wealthy.app"
}

selected = st.selectbox(
    "Select Platform",
    list(apps.keys())
)

try:

    df = fetch_reviews(apps[selected])

    # Check if dataframe is empty
    if df.empty:
        st.error("No reviews found.")
        st.stop()

    # Check if review column exists
    if "review" not in df.columns:
        st.error("Review column missing.")
        st.write(df.head())
        st.stop()

    # Sentiment Analysis
    df["sentiment"] = df["review"].astype(str).apply(analyze_sentiment)

    # Metrics
    st.metric(
        "Average Rating",
        round(df["rating"].mean(), 2)
    )

    st.subheader("Review Data")

    st.dataframe(df)

    st.subheader("Sentiment Distribution")

    st.bar_chart(
        df["sentiment"].value_counts()
    )

except Exception as e:

    st.error(f"Error: {e}")
