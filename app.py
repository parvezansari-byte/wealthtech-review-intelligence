import streamlit as st
import pandas as pd

from scraper.review_scraper import fetch_reviews
from analytics.sentiment import analyze_sentiment

st.set_page_config(
    page_title="WealthTech Review Intelligence",
    layout="wide"
)

st.title("📊 WealthTech Review Intelligence Dashboard")

apps = {
    "NJ Wealth": "com.njindia.finwizard",
    "FundsIndia": "com.fundsindia.consumer"
}

selected = st.selectbox(
    "Select Platform",
    list(apps.keys())
)

df = fetch_reviews(apps[selected])

df["sentiment"] = df["review"].apply(analyze_sentiment)

st.metric(
    "Average Rating",
    round(df["rating"].mean(), 2)
)

st.dataframe(df)

st.bar_chart(
    df["sentiment"].value_counts()
)
