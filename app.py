import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from wordcloud import WordCloud

from analytics.sentiment import analyze_sentiment
from analytics.complaints import detect_issue

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="WealthTech Intelligence Platform",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🚀 WealthTech Review Intelligence Dashboard")

st.markdown("""
AI-powered WealthTech competitor intelligence platform.
Daily updated Play Store review analytics system.
""")

# ---------------------------------------------------
# PLATFORM LIST
# ---------------------------------------------------

apps = {
    "NJ Partner Desk": "com.fin.mpartnerdesk",
    "Prudent": "com.prumob.mobileapp",
    "AssetPlus": "in.assetplus.partner",
    "Wealthy Partner": "in.wealthy.android.advisor",
    "Nuvama": "com.Edelweiss.FPD.edelweiss_subbroker_app",
    "ZFunds Experts": "com.zfunds.experts",
    "FundsIndia Partner": "com.fundsindia.partnerapp",
    "Centricity": "com.centricity_app",
    "Bonanza": "com.bonanzabranch.BranchMbos",
    "Groww": "com.nextbillion.groww",
    "Angel One": "com.msf.angelmobile",
    "Zerodha": "com.zerodha.kite3",
    "Upstox": "in.upstox.pro"
}

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("📱 Platform Selection")

selected = st.sidebar.multiselect(
    "Choose Platforms",
    list(apps.keys()),
    default=list(apps.keys())
)

# ---------------------------------------------------
# LOAD CSV DATA
# ---------------------------------------------------

try:

    final_df = pd.read_csv(
        "data/latest_reviews.csv"
    )

except Exception as e:

    st.error(f"CSV Load Error: {e}")

    st.stop()

# ---------------------------------------------------
# CHECK DATA
# ---------------------------------------------------

if final_df.empty:

    st.error("No review data found.")

    st.stop()

# ---------------------------------------------------
# FILTER PLATFORMS
# ---------------------------------------------------

final_df = final_df[
    final_df["platform"].isin(selected)
]

# ---------------------------------------------------
# CHECK FILTERED DATA
# ---------------------------------------------------

if final_df.empty:

    st.error("No matching platform reviews found.")

    st.stop()

# ---------------------------------------------------
# SENTIMENT ANALYSIS
# ---------------------------------------------------

final_df["sentiment"] = (
    final_df["review"]
    .astype(str)
    .apply(analyze_sentiment)
)

# ---------------------------------------------------
# COMPLAINT DETECTION
# ---------------------------------------------------

final_df["issue_type"] = (
    final_df["review"]
    .astype(str)
    .apply(detect_issue)
)

# ---------------------------------------------------
# SUMMARY TABLE
# ---------------------------------------------------

summary = (
    final_df
    .groupby("platform")
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

# ---------------------------------------------------
# POSITIVE %
# ---------------------------------------------------

positive_scores = []

for platform in summary["Platform"]:

    temp = final_df[
        final_df["platform"] == platform
    ]

    positive_pct = round(
        (temp["sentiment"] == "Positive").mean() * 100,
        1
    )

    positive_scores.append(positive_pct)

summary["Positive %"] = positive_scores
# ---------------------------------------------------
# OVERALL PLATFORM SCORE
# ---------------------------------------------------

# NORMALIZED REVIEW SCORE

max_reviews = (
    summary["Total Reviews"].max()
)

summary["Review Score"] = (
    summary["Total Reviews"] / max_reviews
) * 5

# FINAL WEIGHTED SCORE

summary["Overall Score"] = (

    summary["Avg Rating"] * 0.7 +

    summary["Review Score"] * 0.3

)

summary["Overall Score"] = (
    summary["Overall Score"]
    .round(2)
)

# SORTING

summary = summary.sort_values(
    by="Overall Score",
    ascending=False
)

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------

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
    "⭐ Avg Market Rating",
    round(summary["Avg Rating"].mean(), 2)
)

st.divider()

# ---------------------------------------------------
# LEADERBOARD
# ---------------------------------------------------

st.subheader("🏆 Platform Leaderboard")

st.dataframe(
    summary,
    use_container_width=True
)

# ---------------------------------------------------
# RATING COMPARISON
# ---------------------------------------------------

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

# ---------------------------------------------------
# SENTIMENT COMPARISON
# ---------------------------------------------------

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

# ---------------------------------------------------
# OVERALL SENTIMENT PIE
# ---------------------------------------------------

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

# ---------------------------------------------------
# ISSUE ANALYSIS
# ---------------------------------------------------

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

# ---------------------------------------------------
# WORD CLOUD
# ---------------------------------------------------

st.subheader("☁️ Review Word Cloud")

text = " ".join(
    final_df["review"]
    .astype(str)
)

wordcloud = WordCloud(
    width=1200,
    height=500,
    background_color="black"
).generate(text)

fig, ax = plt.subplots(figsize=(14, 7))

ax.imshow(wordcloud)

ax.axis("off")

st.pyplot(fig)

# ---------------------------------------------------
# AI EXECUTIVE INSIGHTS
# ---------------------------------------------------

st.subheader("🧠 AI Executive Insights")

try:

    # BEST RATING
    best_rating = summary.loc[
        summary["Avg Rating"].idxmax()
    ]

    # BEST SENTIMENT
    best_sentiment = summary.loc[
        summary["Positive %"].idxmax()
    ]

    # TOP ISSUE
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

💡 Platforms with stronger UX, onboarding experience, and app stability are generating significantly higher customer satisfaction.

🏆 The Indian WealthTech ecosystem is rapidly shifting toward:
- AI-powered workflows
- advisor operating systems
- automation-led engagement
- mobile-first financial infrastructure
"""
    )

except Exception as e:

    st.error(f"Insight Engine Error: {e}")

# ---------------------------------------------------
# LIVE DATASET
# ---------------------------------------------------

st.subheader("📋 Daily Updated Review Dataset")

st.dataframe(
    final_df,
    use_container_width=True
)
