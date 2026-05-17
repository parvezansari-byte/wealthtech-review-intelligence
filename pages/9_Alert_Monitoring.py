import streamlit as st
import pandas as pd

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
# PLATFORM CHECKS
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

    # ---------------------------------------------------
    # LOW RATING ALERT
    # ---------------------------------------------------

    if avg_rating < 3.5:

        alerts.append({
            "Platform": platform,
            "Alert Type": "Low Rating",
            "Severity": "High",
            "Message":
                f"{platform} average rating is low ({round(avg_rating,2)})"
        })

    # ---------------------------------------------------
    # HIGH COMPLAINT ALERT
    # ---------------------------------------------------

    negative_reviews = temp[
        temp
