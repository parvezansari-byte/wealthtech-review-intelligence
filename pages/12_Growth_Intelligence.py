import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Growth Intelligence",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📈 Historical Growth Intelligence")

st.markdown("""
Predictive WealthTech momentum and adoption analytics.
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

    st.error("No historical data found.")

    st.stop()

# ---------------------------------------------------
# DATE FORMAT
# ---------------------------------------------------

df["scraped_at"] = pd.to_datetime(
    df["scraped_at"]
)

df["date"] = (
    df["scraped_at"]
    .dt.date
)

# ---------------------------------------------------
# DAILY REVIEW COUNTS
# ---------------------------------------------------

daily_growth = (
    df.groupby([
        "date",
        "platform"
    ])
    .size()
    .reset_index(name="reviews")
)

# ---------------------------------------------------
# GROWTH RATE
# ---------------------------------------------------

daily_growth["Growth Rate"] = (

    daily_growth
    .groupby("platform")["reviews"]
    .pct_change()

) * 100

daily_growth["Growth Rate"] = (
    daily_growth["Growth Rate"]
    .fillna(0)
    .round(2)
)

# ---------------------------------------------------
# REVIEW MOMENTUM CHART
# ---------------------------------------------------

st.subheader("🚀 Platform Momentum")

fig_reviews = px.line(

    daily_growth,

    x="date",

    y="reviews",

    color="platform",

    markers=True,

    title="Daily Review Growth"

)

st.plotly_chart(
    fig_reviews,
    use_container_width=True
)

# ---------------------------------------------------
# GROWTH RATE CHART
# ---------------------------------------------------

st.subheader("📈 Growth Acceleration")

fig_growth = px.line(

    daily_growth,

    x="date",

    y="Growth Rate",

    color="platform",

    markers=True,

    title="Platform Growth Rate (%)"

)

st.plotly_chart(
    fig_growth,
    use_container_width=True
)

# ---------------------------------------------------
# MOMENTUM SCORE
# ---------------------------------------------------

momentum = (
    daily_growth
    .groupby("platform")["reviews"]
    .sum()
    .reset_index()
)

momentum.columns = [
    "Platform",
    "Total Reviews"
]

max_reviews = (
    momentum["Total Reviews"]
    .max()
)

momentum["Momentum Score"] = (

    momentum["Total Reviews"]

    / max_reviews

) * 10

momentum["Momentum Score"] = (
    momentum["Momentum Score"]
    .round(2)
)

# ---------------------------------------------------
# MOMENTUM LEADERBOARD
# ---------------------------------------------------

st.subheader("🏆 Momentum Leaderboard")

momentum = momentum.sort_values(
    by="Momentum Score",
    ascending=False
)

st.dataframe(
    momentum,
    use_container_width=True
)

# ---------------------------------------------------
# MOMENTUM VISUAL
# ---------------------------------------------------

fig_momentum = px.bar(

    momentum,

    x="Platform",

    y="Momentum Score",

    color="Momentum Score",

    text_auto=True,

    title="WealthTech Momentum Index"

)

st.plotly_chart(
    fig_momentum,
    use_container_width=True
)

# ---------------------------------------------------
# MARKET INSIGHTS
# ---------------------------------------------------

st.subheader("🧠 Growth Intelligence Insights")

leader = momentum.iloc[0]

st.info(
    f"""
🚀 {leader['Platform']} currently demonstrates the strongest market momentum.

📈 Higher review velocity generally indicates:
- increasing advisor engagement
- stronger app adoption
- rising platform activity
- growing ecosystem relevance

💡 Momentum analytics can help identify:
- future category leaders
- adoption acceleration
- operational traction
- competitive positioning

🏦 WealthTech platforms with consistent growth momentum are more likely to:
- scale advisor networks
- improve engagement
- strengthen retention
- increase ecosystem influence
"""
)

# ---------------------------------------------------
# RAW DATA
# ---------------------------------------------------

st.subheader("📋 Growth Dataset")

st.dataframe(
    daily_growth,
    use_container_width=True
)
