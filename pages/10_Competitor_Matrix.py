import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Competitor Matrix",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📊 WealthTech Competitor Matrix")

st.markdown("""
Advisor adoption vs platform satisfaction analysis.
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
# PLATFORM SUMMARY
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
# MATRIX CLASSIFICATION
# ---------------------------------------------------

def classify(row):

    if (
        row["Satisfaction Score"] >= 8
        and
        row["Adoption Score"] >= 7
    ):

        return "Leaders"

    elif (
        row["Satisfaction Score"] >= 8
    ):

        return "Innovators"

    elif (
        row["Adoption Score"] >= 7
    ):

        return "Challengers"

    else:

        return "Niche Players"

summary["Category"] = (
    summary.apply(
        classify,
        axis=1
    )
)

# ---------------------------------------------------
# MATRIX CHART
# ---------------------------------------------------

fig = px.scatter(

    summary,

    x="Adoption Score",

    y="Satisfaction Score",

    size="Total Reviews",

    color="Category",

    hover_name="Platform",

    text="Platform",

    title="WealthTech Competitive Positioning Matrix"

)

fig.update_traces(
    textposition="top center"
)

# ---------------------------------------------------
# DISPLAY
# ---------------------------------------------------

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# CATEGORY TABLE
# ---------------------------------------------------

st.subheader("🏆 Competitive Classification")

st.dataframe(
    summary[[
        "Platform",
        "Avg Rating",
        "Total Reviews",
        "Adoption Score",
        "Satisfaction Score",
        "Category"
    ]],
    use_container_width=True
)

# ---------------------------------------------------
# STRATEGIC INSIGHTS
# ---------------------------------------------------

st.subheader("🧠 Strategic Market Insights")

leaders = summary[
    summary["Category"] == "Leaders"
]

innovators = summary[
    summary["Category"] == "Innovators"
]

challengers = summary[
    summary["Category"] == "Challengers"
]

st.info(
    f"""
🏆 Leaders:
{len(leaders)} platforms currently dominate both advisor adoption and satisfaction.

🚀 Innovators:
{len(innovators)} platforms show strong customer satisfaction but lower scale.

📈 Challengers:
{len(challengers)} platforms have large user bases but require UX and product improvements.

💡 The WealthTech ecosystem is increasingly rewarding:
- mobile-first workflows
- advisor automation
- platform stability
- onboarding simplicity
- intelligent engagement systems
"""
)
