import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Alert Monitoring",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🚨 Real-Time Alert & Monitoring Engine")

st.markdown("""
Automated WealthTech platform health monitoring.
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

# ---------------------------------------------------
# ALERT STORAGE
# ---------------------------------------------------

alerts = []

# ---------------------------------------------------
# PLATFORM ANALYSIS
# ---------------------------------------------------

platforms = df["platform"].unique()

for platform in platforms:

    temp = df[
        df["platform"] == platform
    ]

    avg_rating = (
        temp["rating"].mean()
    )

    total_reviews = len(temp)

    negative_reviews = temp[
        temp["rating"] <= 2
    ]

    negative_pct = (
        len(negative_reviews)
        / total_reviews
    ) * 100

    # ---------------------------------------------------
    # LOW RATING ALERT
    # ---------------------------------------------------

    if avg_rating < 3.5:

        alerts.append({

            "Platform": platform,

            "Alert Type": "Low Rating",

            "Severity": "High",

            "Message":
                f"{platform} rating dropped to {round(avg_rating,2)}"

        })

    # ---------------------------------------------------
    # NEGATIVE REVIEW ALERT
    # ---------------------------------------------------

    if negative_pct > 30:

        alerts.append({

            "Platform": platform,

            "Alert Type": "Negative Review Spike",

            "Severity": "Critical",

            "Message":
                f"{platform} has {round(negative_pct,1)}% negative reviews"

        })

    # ---------------------------------------------------
    # LOW ENGAGEMENT ALERT
    # ---------------------------------------------------

    if total_reviews < 5:

        alerts.append({

            "Platform": platform,

            "Alert Type": "Low Engagement",

            "Severity": "Medium",

            "Message":
                f"{platform} has low review activity"

        })

# ---------------------------------------------------
# ALERT DATAFRAME
# ---------------------------------------------------

alerts_df = pd.DataFrame(alerts)

# ---------------------------------------------------
# NO ALERTS
# ---------------------------------------------------

if alerts_df.empty:

    st.success(
        "✅ No major platform risks detected."
    )

else:

    # ---------------------------------------------------
    # ALERT TABLE
    # ---------------------------------------------------

    st.subheader("🚨 Active Platform Alerts")

    st.dataframe(
        alerts_df,
        use_container_width=True
    )

    # ---------------------------------------------------
    # ALERT CHART
    # ---------------------------------------------------

    alert_counts = (
        alerts_df["Severity"]
        .value_counts()
        .reset_index()
    )

    alert_counts.columns = [
        "Severity",
        "Count"
    ]

    fig = px.bar(

        alert_counts,

        x="Severity",

        y="Count",

        color="Severity",

        text_auto=True,

        title="Platform Risk Severity"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------
# PLATFORM HEALTH TABLE
# ---------------------------------------------------

st.subheader("📊 Platform Health Summary")

health = (
    df.groupby("platform")
    .agg({
        "rating": ["mean", "count"]
    })
)

health.columns = [
    "Avg Rating",
    "Total Reviews"
]

health = health.reset_index()

health["Avg Rating"] = (
    health["Avg Rating"]
    .round(2)
)

st.dataframe(
    health,
    use_container_width=True
)
