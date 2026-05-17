import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from wordcloud import WordCloud

from scraper.review_scraper import fetch_reviews
from analytics.sentiment import analyze_sentiment

# PAGE CONFIG
st.set_page_config(
    page_title="WealthTech Review Intelligence",
    layout="wide"
)

# TITLE
st.title("📊 WealthTech Review Intelligence Dashboard")

# SIDEBAR
st.sidebar.header("Platform Selection")

apps = {
    "Groww": "com.nextbillion.groww",
    "Angel One": "com.msf.angelmobile",
    "Zerodha": "com.zerodha.kite3",
    "Upstox": "in.upstox.pro"
}

selected = st.sidebar.selectbox(
    "Choose Platform",
    list(apps.keys())
)

# FETCH DATA
df = fetch_reviews(apps[selected])

# CHECK EMPTY
if df.empty:
    st.error("No reviews found.")
    st.stop()

# SENTIMENT
df["sentiment"] = df["review"].astype(str).apply(analyze_sentiment)

# METRICS
avg_rating = round(df["rating"].mean(), 2)
total_reviews = len(df)

positive_pct = round(
    (df["sentiment"] == "Positive").mean() * 100,
    1
)

negative_pct = round(
    (df["sentiment"] == "Negative").mean() * 100,
    1
)

# KPI ROW
col1, col2, col3, col4 = st.columns(4)

col1.metric("⭐ Avg Rating", avg_rating)
col2.metric("📝 Total Reviews", total_reviews)
col3.metric("😊 Positive %", f"{positive_pct}%")
col4.metric("😡 Negative %", f"{negative_pct}%")

st.divider()

# SENTIMENT COUNTS
sentiment_counts = (
    df["sentiment"]
    .value_counts()
    .reset_index()
)

sentiment_counts.columns = [
    "Sentiment",
    "Count"
]

# PIE CHART
fig_pie = px.pie(
    sentiment_counts,
    names="Sentiment",
    values="Count",
    title="Sentiment Distribution"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

# RATING DISTRIBUTION
fig_bar = px.histogram(
    df,
    x="rating",
    title="Ratings Distribution"
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# WORD CLOUD
st.subheader("☁️ Review Word Cloud")

text = " ".join(df["review"].astype(str))

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="black"
).generate(text)

fig, ax = plt.subplots()

ax.imshow(wordcloud)

ax.axis("off")

st.pyplot(fig)

# REVIEW TABLE
st.subheader("📋 Review Dataset")

st.dataframe(df)
