import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    layout="wide"
)

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

    st.error("No historical data found.")

    st.stop()

# ---------------------------------------------------
# SUMMARY
# ---------------------------------------------------

summary = (
    df.groupby("platform")
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
# METRICS
# ---------------------------------------------------

total_platforms = len(summary)

total_reviews = len(df)

market_rating = round(
    summary["Avg Rating"].mean(),
    2
)

top_platform = summary.loc[
    summary["Avg Rating"].idxmax()
]

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🏦 WealthTech Intelligence Command Center")

st.markdown("""
Institutional analytics infrastructure for WealthTech platforms.
""")

# ---------------------------------------------------
# KPI ROW
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📱 Platforms",
    total_platforms
)

col2.metric(
    "📝 Reviews",
    total_reviews
)

col3.metric(
    "⭐ Market Avg Rating",
    market_rating
)

col4.metric(
    "🏆 Market Leader",
    top_platform["Platform"]
)

st.divider()

# ---------------------------------------------------
# TOP LEADERBOARD
# ---------------------------------------------------

st.subheader("🏆 Market Leaderboard")

leaderboard = summary.sort_values(
    by="Avg Rating",
    ascending=False
)

fig_leaderboard = px.bar(

    leaderboard,

    x="Platform",

    y="Avg Rating",

    color="Avg Rating",

    text_auto=True,

    title="Top WealthTech Platforms"

)

st.plotly_chart(
    fig_leaderboard,
    use_container_width=True
)

# ---------------------------------------------------
# REVIEW DISTRIBUTION
# ---------------------------------------------------

st.subheader("📊 Review Distribution")

fig_reviews = px.pie(

    summary,

    names="Platform",

    values="Total Reviews",

    title="Market Review Share"

)

st.plotly_chart(
    fig_reviews,
    use_container_width=True
)

# ---------------------------------------------------
# PLATFORM TABLE
# ---------------------------------------------------

st.subheader("📋 Executive Intelligence Table")

st.dataframe(
    leaderboard,
    use_container_width=True
)

# ---------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------

st.subheader("🧠 Executive Market Insights")

st.info(
    f"""
🏆 {top_platform['Platform']} currently leads the WealthTech ecosystem based on platform ratings.

📈 Market dynamics indicate increasing demand for:
- mobile-first advisory systems
- automation-led engagement
- scalable onboarding
- operational stability
- advisor-centric workflows

🚀 Platforms with superior UX and lower friction are gaining faster advisor adoption.

💡 The WealthTech ecosystem is rapidly evolving toward intelligent advisor operating systems and embedded financial infrastructure.
"""
)

# ---------------------------------------------------
# RECENT REVIEWS
# ---------------------------------------------------

st.subheader("📰 Recent Market Activity")

recent_reviews = df.tail(10)

st.dataframe(
    recent_reviews,
    use_container_width=True
)
