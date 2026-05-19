import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Complaint Heatmap",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🔥 AI Complaint Heatmap Intelligence")

st.markdown("""
Operational risk and complaint analytics engine.
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
# CATEGORY ENGINE
# ---------------------------------------------------

def detect_issue(text):

    text = str(text).lower()

    if any(word in text for word in [

        "login",
        "otp",
        "password"

    ]):

        return "Login Issues"

    elif any(word in text for word in [

        "crash",
        "bug",
        "hang",
        "slow"

    ]):

        return "Performance"

    elif any(word in text for word in [

        "kyc",
        "verification",
        "onboarding"

    ]):

        return "KYC"

    elif any(word in text for word in [

        "support",
        "service",
        "response"

    ]):

        return "Support"

    else:

        return "General"

# ---------------------------------------------------
# APPLY ISSUE ENGINE
# ---------------------------------------------------

df["Issue"] = (

    df["review"]

    .astype(str)

    .apply(detect_issue)

)

# ---------------------------------------------------
# HEATMAP DATA
# ---------------------------------------------------

heatmap_data = (

    df.groupby([

        "platform",

        "Issue"

    ])

    .size()

    .reset_index(name="Count")

)

# ---------------------------------------------------
# PIVOT
# ---------------------------------------------------

pivot = heatmap_data.pivot(

    index="platform",

    columns="Issue",

    values="Count"

).fillna(0)

# ---------------------------------------------------
# HEATMAP
# ---------------------------------------------------

fig = px.imshow(

    pivot,

    text_auto=True,

    aspect="auto",

    title="Platform Complaint Heatmap"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# ---------------------------------------------------
# RAW TABLE
# ---------------------------------------------------

st.subheader("📊 Complaint Intelligence Table")

st.dataframe(

    pivot,

    use_container_width=True

)

# ---------------------------------------------------
# EXECUTIVE INSIGHTS
# ---------------------------------------------------

st.subheader("🧠 AI Risk Insights")

top_issue = (

    heatmap_data

    .groupby("Issue")["Count"]

    .sum()

    .reset_index()

)

top_issue = top_issue.sort_values(

    by="Count",

    ascending=False

)

most_common = top_issue.iloc[0]

st.info(
    f"""
🚨 Most common ecosystem issue:
{most_common['Issue']}

📈 Complaint heatmaps help identify:
- operational weaknesses
- onboarding friction
- login instability
- support gaps
- platform risk concentration

🏦 WealthTech platforms with lower complaint intensity generally demonstrate:
- stronger retention
- better UX
- higher advisor satisfaction
- better scalability
"""
)
