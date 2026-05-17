import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Trend Analytics",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📈 Trend Analytics Engine")

st.markdown("""
Historical intelligence and platform momentum tracking.
""")

# ---------------------------------------------------
# LOAD HISTORICAL DATA
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
# DATE CONVERSION
# ---------------------------------------------------

df["scraped_at"] = pd.to_datetime(
    df["scraped_at"]
)

df["date"] = df["scraped_at"].dt.date

# ---------------------------------------------------
# DAILY REVIEW COUNT
# ---------------------------------------------------

daily_reviews = (
    df.groupby([
        "date",
        "platform"
    ])
    .size()
    .reset_index(name="reviews")
)

# ---------------------------------------------------
# REVIEW TREND CHART
# ---------------------------------------------------

st.subheader("📊 Daily Review Volume")

fig_reviews = px.line(
    daily_reviews,
    x="date",
    y="reviews",
    color="platform",
    markers=True,
    title="Daily Review Activity"
)

st.plotly_chart(
    fig_reviews,
    use_container_width=True
)

# ---------------------------------------------------
# DAILY AVERAGE RATING
# ---------------------------------------------------

daily_rating = (
    df.groupby([
        "date",
        "platform"
    ])["rating"]
    .mean()
    .reset_index()
)

# ---------------------------------------------------
# RATING TREND
# ---------------------------------------------------

st.subheader("⭐ Rating Trend")

fig_rating = px.line(
    daily_rating,
    x="date",
    y="rating",
    color="platform",
    markers=True,
    title="Average Rating Movement"
)

st.plotly_chart(
    fig_rating,
    use_container_width=True
)

# ---------------------------------------------------
# PLATFORM MOMENTUM
# ---------------------------------------------------

momentum = (
    df.groupby("platform")
    .size()
    .reset_index(name="total_reviews")
)

momentum = momentum.sort_values(
    by="total_reviews",
    ascending=False
)

# ---------------------------------------------------
# MOMENTUM CHART
# ---------------------------------------------------

st.subheader("🚀 Platform Momentum")

fig_momentum = px.bar(
    momentum,
    x="platform",
    y="total_reviews",
    title="Total Historical Review Volume",
    text_auto=True
)

st.plotly_chart(
    fig_momentum,
    use_container_width=True
)

# ---------------------------------------------------
# MARKET INSIGHTS
# ---------------------------------------------------

st.subheader("🧠 Trend Insights")

top_platform = momentum.iloc[0]

st.info(
    f"""
🚀 {top_platform['platform']} currently shows the strongest market engagement based on historical review activity.

📈 Increasing review frequency generally indicates:
- higher customer engagement
- stronger app usage
- rapid platform adoption
- growing advisor activity

💡 Trend analytics can help identify:
- platform momentum
- customer satisfaction shifts
- onboarding friction
- operational stability trends
"""
)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------

st.subheader("📋 Historical Dataset")

st.dataframe(
    df,
    use_container_width=True
)
