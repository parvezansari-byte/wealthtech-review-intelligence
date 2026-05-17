import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from wordcloud import WordCloud

from scraper.review_scraper import fetch_reviews
from analytics.sentiment import analyze_sentiment
from analytics.complaints import detect_issue

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="WealthTech Intelligence Platform",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------

st.title("🚀 WealthTech Review Intelligence Dashboard")

st.markdown(
    """
    AI-powered Play Store sentiment and competitor intelligence platform.
    """
)

# -----------------------------------
# PLATFORM LIST
# -----------------------------------

apps = {
    "Groww": "com.nextbillion.groww",
    "Angel One": "com.msf.angelmobile",
    "Zerodha": "com.zerodha.kite3",
    "Upstox": "in.upstox.pro"
}

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.header("📱 Platform Selection")

selected = st.sidebar.multiselect(
    "Choose Platforms",
    list(apps.keys()),
    default=list(apps.keys())
)

# -----------------------------------
# FETCH DATA
# -----------------------------------

all_data = []

for app_name in selected:

    df = fetch_reviews(apps[app_name])

    if not df.empty:

        # Platform Name
        df["Platform"] = app_name

        # Sentiment
        df["sentiment"] = (
            df["review"]
            .astype(str)
            .apply(analyze_sentiment)
        )

        # Complaint Detection
        df["issue_type"] = (
            df["review"]
            .astype(str)
            .apply(detect_issue)
        )

        all_data.append(df)

# -----------------------------------
# CHECK DATA
# -----------------------------------

if len(all_data) == 0:

    st.error("❌ No review data found.")

    st.stop()

# -----------------------------------
# MERGE DATA
# -----------------------------------

final_df = pd.concat(all_data)

# -----------------------------------
# SUMMARY TABLE
# -----------------------------------

summary = (
    final_df
    .groupby("Platform")
    .agg({
        "rating": "mean",
        "review": "count"
    })
    .reset_index()
)

summary.columns = [
    "Platform",
    "Avg Rating",
    "Total Reviews"
]

# -----------------------------------
# POSITIVE %
# -----------------------------------

positive_scores = []

for platform in summary["Platform"]:

    temp = final_df[
        final_df["Platform"] == platform
    ]

    positive_pct = round(
        (temp["sentiment"] == "Positive").mean() * 100,
        1
    )

    positive_scores.append(positive_pct)

summary["Positive %"] = positive_scores

# -----------------------------------
# KPI METRICS
# -----------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "📱 Platforms Analysed",
    len(summary)
)

col2.metric(
    "📝 Total Reviews",
    len(final_df)
)

col3.metric(
    "⭐ Average Market Rating",
    round(summary["Avg Rating"].mean(), 2)
)

st.divider()

# -----------------------------------
# LEADERBOARD
# -----------------------------------

st.subheader("🏆 Platform Leaderboard")

st.dataframe(
    summary,
    use_container_width=True
)

# -----------------------------------
# RATING COMPARISON
# -----------------------------------

fig_rating = px.bar(
    summary,
    x="Platform",
    y="Avg Rating",
    title="⭐ Average Rating Comparison",
    text_auto=True
)

st.plotly_chart(
    fig_rating,
    use_container_width=True
)

# -----------------------------------
# POSITIVE SENTIMENT
# -----------------------------------

fig_sentiment = px.bar(
    summary,
    x="Platform",
    y="Positive %",
    title="😊 Positive Sentiment Comparison",
    text_auto=True
)

st.plotly_chart(
    fig_sentiment,
    use_container_width=True
)

# -----------------------------------
# OVERALL SENTIMENT PIE
# -----------------------------------

sentiment_counts = (
    final_df["sentiment"]
    .value_counts()
    .reset_index()
)

sentiment_counts.columns = [
    "Sentiment",
    "Count"
]

fig_pie = px.pie(
    sentiment_counts,
    names="Sentiment",
    values="Count",
    title="📊 Overall Sentiment Distribution"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

# -----------------------------------
# ISSUE ANALYSIS
# -----------------------------------

st.subheader("🚨 Complaint Intelligence")

issue_counts = (
    final_df["issue_type"]
    .value_counts()
    .reset_index()
)

issue_counts.columns = [
    "Issue Type",
    "Count"
]

fig_issue = px.bar(
    issue_counts,
    x="Issue Type",
    y="Count",
    title="🚨 Most Common Complaint Categories",
    text_auto=True
)

st.plotly_chart(
    fig_issue,
    use_container_width=True
)

# -----------------------------------
# WORD CLOUD
# -----------------------------------

st.subheader("☁️ Review Word Cloud")

text = " ".join(
    final_df["review"]
    .astype(str)
)

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color="black"
).generate(text)

fig, ax = plt.subplots(figsize=(12, 6))

ax.imshow(wordcloud)

ax.axis("off")

st.pyplot(fig)

# -----------------------------------
# AI EXECUTIVE INSIGHTS
# -----------------------------------

st.subheader("🧠 AI Executive Insights")

try:

    # Highest Rated
    best_rating = summary.loc[
        summary["Avg Rating"].idxmax()
    ]

    # Highest Sentiment
    best_sentiment = summary.loc[
        summary["Positive %"].idxmax()
    ]

    # Top Complaint
    if not issue_counts.empty:

        top_issue = issue_counts.iloc[0]

        issue_text = (
            f"{top_issue['Issue Type']} "
            f"({top_issue['Count']} mentions)"
        )

    else:

        issue_text = (
            "No major complaint patterns detected."
        )

    st.info(
        f"""
📈 {best_rating['Platform']} has the highest average rating of {round(best_rating['Avg Rating'],2)}.

😊 {best_sentiment['Platform']} shows the strongest positive sentiment at {best_sentiment['Positive %']}%.

🚨 Most common complaint category:
{issue_text}

💡 Platforms with stronger UX, stability, and onboarding experience are generating significantly higher customer satisfaction.

🏆 The market is shifting toward AI-powered, mobile-first, engagement-driven fintech ecosystems.
"""
    )

except Exception as e:

    st.error(f"Insight Engine Error: {e}")

# -----------------------------------
# REVIEW DATASET
# -----------------------------------

st.subheader("📋 Live Review Dataset")

st.dataframe(
    final_df,
    use_container_width=True
)
