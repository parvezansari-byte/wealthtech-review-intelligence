import streamlit as st
import pandas as pd
import plotly.express as px

from scraper.review_scraper import fetch_reviews
from analytics.sentiment import analyze_sentiment
from analytics.complaints import detect_issue

# PAGE CONFIG
st.set_page_config(
    page_title="WealthTech Intelligence Platform",
    layout="wide"
)

# TITLE
st.title("🚀 WealthTech Competitive Intelligence Dashboard")

# APPS
apps = {
    "Groww": "com.nextbillion.groww",
    "Angel One": "com.msf.angelmobile",
    "Zerodha": "com.zerodha.kite3",
    "Upstox": "in.upstox.pro"
}

# SIDEBAR
selected = st.sidebar.multiselect(
    "Select Platforms",
    list(apps.keys()),
    default=list(apps.keys())
)

all_data = []

# FETCH DATA
for app_name in selected:

    df = fetch_reviews(apps[app_name])

    if not df.empty:

        df["Platform"] = app_name

        df["sentiment"] = (
            df["review"]
            .astype(str)
            .apply(analyze_sentiment)
        )

        df["issue_type"] = (
            df["review"]
            .astype(str)
            .apply(detect_issue)
        )

        all_data.append(df)

# CHECK DATA
if len(all_data) == 0:
    st.error("No review data found.")
    st.stop()

# MERGE
final_df = pd.concat(all_data)

# KPI TABLE
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

# SENTIMENT %
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

# SHOW TABLE
st.subheader("🏆 Platform Leaderboard")

st.dataframe(summary)

# RATING COMPARISON
fig_rating = px.bar(
    summary,
    x="Platform",
    y="Avg Rating",
    title="Average Rating Comparison",
    text_auto=True
)

st.plotly_chart(
    fig_rating,
    use_container_width=True
)

# POSITIVE SENTIMENT
fig_sentiment = px.bar(
    summary,
    x="Platform",
    y="Positive %",
    title="Positive Sentiment Comparison",
    text_auto=True
)

st.plotly_chart(
    fig_sentiment,
    use_container_width=True
)

# PIE CHART
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
    title="Overall Sentiment Distribution"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)
# AI INSIGHTS
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

    # ISSUE ANALYSIS SAFE CHECK
    if not issue_counts.empty:

        top_issue = issue_counts.iloc[0]

        issue_text = (
            f"{top_issue['Issue Type']} "
            f"({top_issue['Count']} mentions)"
        )

    else:

        issue_text = "No major complaint patterns detected."

    # DISPLAY INSIGHTS
    st.info(
        f'''
📈 {best_rating["Platform"]} has the highest average rating of {round(best_rating["Avg Rating"],2)}.

😊 {best_sentiment["Platform"]} shows the strongest positive sentiment at {best_sentiment["Positive %"]}%.

🚨 Most common complaint category:
{issue_text}

💡 Platforms with stronger UX and stability are generating significantly higher customer satisfaction.
'''
    )

except Exception as e:

    st.error(f"Insight Engine Error: {e}")
# BEST RATING
best_rating = summary.loc[
    summary["Avg Rating"].idxmax()
]

# BEST SENTIMENT
best_sentiment = summary.loc[
    summary["Positive %"].idxmax()
]

# MOST COMPLAINTS
top_issue = issue_counts.iloc[0]

st.info(
    f"""
    📈 {best_rating['Platform']} has the highest average rating of {round(best_rating['Avg Rating'],2)}.

    😊 {best_sentiment['Platform']} shows the strongest positive sentiment at {best_sentiment['Positive %']}%.

    🚨 Most common complaint category across platforms:
    {top_issue['Issue Type']} ({top_issue['Count']} mentions).

    💡 Platforms with stronger UX and stability are generating significantly higher user satisfaction.
    """
)
# ISSUE ANALYSIS
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
    title="Most Common Complaints",
    text_auto=True
)

st.plotly_chart(
    fig_issue,
    use_container_width=True
)

# REVIEW DATA
st.subheader("📋 Live Review Dataset")

st.dataframe(final_df)
