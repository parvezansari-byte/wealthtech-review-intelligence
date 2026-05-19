import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Benchmarking",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🧠 AI Executive Benchmarking Engine")

st.markdown("""
Founder and investor-grade WealthTech benchmarking intelligence.
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
# PLATFORM SUMMARY
# ---------------------------------------------------

summary = (

    df.groupby("platform")

    .agg({

        "rating": "mean",

        "review": "count",

        "likes": "sum"

    })

    .reset_index()

)

summary.columns = [

    "Platform",

    "Average Rating",

    "Total Reviews",

    "Total Likes"

]

# ---------------------------------------------------
# NORMALIZED SCORING
# ---------------------------------------------------

summary["Review Score"] = (

    summary["Total Reviews"]

    / summary["Total Reviews"].max()

) * 100

summary["Rating Score"] = (

    summary["Average Rating"]

    / 5

) * 100

summary["Engagement Score"] = (

    summary["Total Likes"]

    / summary["Total Likes"].max()

) * 100

# ---------------------------------------------------
# FINAL BENCHMARK SCORE
# ---------------------------------------------------

summary["Benchmark Score"] = (

    summary["Review Score"] * 0.4

    +

    summary["Rating Score"] * 0.4

    +

    summary["Engagement Score"] * 0.2

)

summary["Benchmark Score"] = (

    summary["Benchmark Score"]

    .round(2)

)

# ---------------------------------------------------
# SORTING
# ---------------------------------------------------

summary = summary.sort_values(

    by="Benchmark Score",

    ascending=False

)

# ---------------------------------------------------
# RANKING
# ---------------------------------------------------

summary["Rank"] = range(

    1,

    len(summary) + 1

)

# ---------------------------------------------------
# BENCHMARK TABLE
# ---------------------------------------------------

st.subheader("🏆 Executive Benchmark Ranking")

st.dataframe(

    summary[[

        "Rank",

        "Platform",

        "Average Rating",

        "Total Reviews",

        "Total Likes",

        "Benchmark Score"

    ]],

    use_container_width=True

)

# ---------------------------------------------------
# VISUAL RANKING
# ---------------------------------------------------

fig = px.bar(

    summary,

    x="Platform",

    y="Benchmark Score",

    color="Benchmark Score",

    text="Benchmark Score",

    title="AI Executive Benchmarking"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ---------------------------------------------------
# SWOT ENGINE
# ---------------------------------------------------

st.subheader("🧠 AI SWOT Intelligence")

for _, row in summary.iterrows():

    platform = row["Platform"]

    rating = row["Average Rating"]

    reviews = row["Total Reviews"]

    score = row["Benchmark Score"]

    # ---------------------------------------------------
    # STRENGTH
    # ---------------------------------------------------

    if rating >= 4:

        strength = (
            "Strong customer satisfaction and UX."
        )

    else:

        strength = (
            "Moderate customer perception."
        )

    # ---------------------------------------------------
    # WEAKNESS
    # ---------------------------------------------------

    if rating < 3.5:

        weakness = (
            "Platform stability and onboarding friction risk."
        )

    else:

        weakness = (
            "Requires deeper ecosystem expansion."
        )

    # ---------------------------------------------------
    # OPPORTUNITY
    # ---------------------------------------------------

    if reviews > 100:

        opportunity = (
            "Strong potential for advisor ecosystem scaling."
        )

    else:

        opportunity = (
            "Opportunity to improve advisor acquisition."
        )

    # ---------------------------------------------------
    # RISK
    # ---------------------------------------------------

    if score < 60:

        risk = (
            "Competitive positioning risk increasing."
        )

    else:

        risk = (
            "Healthy market positioning."
        )

    # ---------------------------------------------------
    # DISPLAY
    # ---------------------------------------------------

    st.info(
        f"""
🏢 Platform: {platform}

✅ Strength:
{strength}

⚠️ Weakness:
{weakness}

🚀 Opportunity:
{opportunity}

🚨 Risk:
{risk}

📈 Benchmark Score:
{score}
"""
    )

# ---------------------------------------------------
# EXECUTIVE MARKET INSIGHTS
# ---------------------------------------------------

st.subheader("📊 Executive Market Commentary")

leader = summary.iloc[0]

st.success(
    f"""
🏆 {leader['Platform']} currently leads the WealthTech benchmarking index.

📈 Platforms with higher benchmark scores generally demonstrate:
- superior advisor experience
- stronger onboarding
- better operational scalability
- higher customer engagement
- improved product-market fit

💡 AI benchmarking intelligence helps:
- founders
- investors
- product teams
- fintech operators
- strategy consultants

understand WealthTech competitive positioning.
"""
)
