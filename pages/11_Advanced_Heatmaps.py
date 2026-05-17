import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Advanced Heatmaps",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🔥 Advanced Heatmap Intelligence")

st.markdown("""
Institutional WealthTech visual analytics engine.
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
# SUMMARY
# ---------------------------------------------------

summary = (
    df.groupby("platform")
    .agg({
        "rating": ["mean", "count"]
    })
)

summary.columns = [
    "Avg Rating",
    "Total Reviews"
]

summary = summary.reset_index()

# ---------------------------------------------------
# SATISFACTION SCORE
# ---------------------------------------------------

summary["Satisfaction Score"] = (
    summary["Avg Rating"] * 2
)

# ---------------------------------------------------
# ADOPTION SCORE
# ---------------------------------------------------

max_reviews = (
    summary["Total Reviews"].max()
)

summary["Adoption Score"] = (

    summary["Total Reviews"]

    / max_reviews

) * 10

# ---------------------------------------------------
# STABILITY SCORE
# ---------------------------------------------------

summary["Stability Score"] = (
    summary["Avg Rating"] * 1.8
)

# ---------------------------------------------------
# INNOVATION SCORE
# ---------------------------------------------------

summary["Innovation Score"] = (

    summary["Satisfaction Score"] * 0.6 +

    summary["Adoption Score"] * 0.4

)

# ---------------------------------------------------
# HEATMAP DATA
# ---------------------------------------------------

heatmap_df = summary[[
    "platform",
    "Avg Rating",
    "Adoption Score",
    "Satisfaction Score",
    "Stability Score",
    "Innovation Score"
]]

# ---------------------------------------------------
# MELT
# ---------------------------------------------------

melted = heatmap_df.melt(

    id_vars="platform",

    var_name="Metric",

    value_name="Score"
)

# ---------------------------------------------------
# HEATMAP
# ---------------------------------------------------

fig = px.imshow(

    melted.pivot(
        index="platform",
        columns="Metric",
        values="Score"
    ),

    text_auto=True,

    aspect="auto",

    title="WealthTech Intelligence Heatmap"
)

# ---------------------------------------------------
# DISPLAY
# ---------------------------------------------------

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# PLATFORM SCORECARD
# ---------------------------------------------------

st.subheader("📊 Platform Intelligence Scorecard")

st.dataframe(
    heatmap_df,
    use_container_width=True
)

# ---------------------------------------------------
# TOP PERFORMERS
# ---------------------------------------------------

st.subheader("🏆 Top Intelligence Leaders")

top_innovation = summary.loc[
    summary["Innovation Score"].idxmax()
]

top_stability = summary.loc[
    summary["Stability Score"].idxmax()
]

top_adoption = summary.loc[
    summary["Adoption Score"].idxmax()
]

col1, col2, col3 = st.columns(3)

col1.metric(
    "🚀 Innovation Leader",
    top_innovation["platform"]
)

col2.metric(
    "🛡 Stability Leader",
    top_stability["platform"]
)

col3.metric(
    "📈 Adoption Leader",
    top_adoption["platform"]
)

# ---------------------------------------------------
# EXECUTIVE INSIGHTS
# ---------------------------------------------------

st.subheader("🧠 Heatmap Intelligence Insights")

st.info(
    f"""
🚀 {top_innovation['platform']} currently leads in innovation perception and advisor satisfaction.

🛡 {top_stability['platform']} demonstrates the strongest operational stability profile.

📈 {top_adoption['platform']} dominates advisor engagement and market activity.

💡 Heatmap analytics reveal how WealthTech platforms compete across:
- customer satisfaction
- operational strength
- scalability
- engagement
- advisor adoption

🏦 Institutional platforms increasingly differentiate through:
- mobile-first infrastructure
- advisor automation
- onboarding efficiency
- operational reliability
"""
)
