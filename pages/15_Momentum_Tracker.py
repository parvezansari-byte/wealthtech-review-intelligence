import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Momentum Tracker",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📈 WealthTech Momentum Tracker")

st.markdown("""
Platform growth and engagement intelligence engine.
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
# DATE CONVERSION
# ---------------------------------------------------

df["review_date"] = pd.to_datetime(
    df["review_date"],
    errors="coerce"
)

# ---------------------------------------------------
# MONTH EXTRACTION
# ---------------------------------------------------

df["Month"] = (
    df["review_date"]
    .dt.strftime("%Y-%m")
)

# ---------------------------------------------------
# MONTHLY REVIEW COUNTS
# ---------------------------------------------------

monthly_growth = (

    df.groupby([

        "Month",

        "platform"

    ])

    .size()

    .reset_index(name="Reviews")

)

# ---------------------------------------------------
# MOMENTUM SCORE
# ---------------------------------------------------

momentum_scores = (

    monthly_growth

    .groupby("platform")["Reviews"]

    .sum()

    .reset_index()

)

momentum_scores.columns = [

    "Platform",

    "Total Reviews"

]

# ---------------------------------------------------
# NORMALIZED SCORE
# ---------------------------------------------------

max_reviews = (
    momentum_scores["Total Reviews"]
    .max()
)

momentum_scores["Momentum Score"] = (

    momentum_scores["Total Reviews"]

    / max_reviews

) * 100

momentum_scores["Momentum Score"] = (

    momentum_scores["Momentum Score"]

    .round(2)

)

# ---------------------------------------------------
# SORTING
# ---------------------------------------------------

momentum_scores = momentum_scores.sort_values(

    by="Momentum Score",

    ascending=False

)

# ---------------------------------------------------
# KPI
# ---------------------------------------------------

top_platform = momentum_scores.iloc[0]

col1, col2 = st.columns(2)

col1.metric(
    "🚀 Top Momentum Platform",
    top_platform["Platform"]
)

col2.metric(
    "📈 Momentum Score",
    top_platform["Momentum Score"]
)

# ---------------------------------------------------
# MOMENTUM TABLE
# ---------------------------------------------------

st.subheader("🏆 Platform Momentum Ranking")

st.dataframe(

    momentum_scores,

    use_container_width=True

)

# ---------------------------------------------------
# MOMENTUM CHART
# ---------------------------------------------------

fig_bar = px.bar(

    momentum_scores,

    x="Platform",

    y="Momentum Score",

    color="Momentum Score",

    text="Momentum Score",

    title="WealthTech Momentum Intelligence"

)

st.plotly_chart(

    fig_bar,

    use_container_width=True

)

# ---------------------------------------------------
# MONTHLY TREND
# ---------------------------------------------------

st.subheader("📊 Monthly Growth Trends")

fig_line = px.line(

    monthly_growth,

    x="Month",

    y="Reviews",

    color="platform",

    markers=True,

    title="Monthly Platform Review Growth"

)

st.plotly_chart(

    fig_line,

    use_container_width=True

)

# ---------------------------------------------------
# HEATMAP
# ---------------------------------------------------

pivot = monthly_growth.pivot(

    index="platform",

    columns="Month",

    values="Reviews"

).fillna(0)

fig_heatmap = px.imshow(

    pivot,

    text_auto=True,

    aspect="auto",

    title="Monthly Growth Heatmap"

)

st.plotly_chart(

    fig_heatmap,

    use_container_width=True

)

# ---------------------------------------------------
# AI INSIGHTS
# ---------------------------------------------------

st.subheader("🧠 Momentum Intelligence Insights")

st.info(
    f"""
🚀 {top_platform['Platform']} currently demonstrates the strongest growth momentum in the WealthTech ecosystem.

📈 Momentum analytics help identify:
- fast-growing platforms
- advisor adoption acceleration
- ecosystem engagement
- product traction
- operational scalability

🏦 Platforms with sustained momentum generally benefit from:
- strong onboarding
- better UX
- platform stability
- advisor-centric workflows
- automation-led engagement
"""
)
