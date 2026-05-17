import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Review Explorer",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("📝 WealthTech Review Explorer")

st.markdown(
    "Platform-wise review intelligence and categorization engine."
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

    st.error("No review data found.")

    st.stop()

# ---------------------------------------------------
# MISSING COLUMN FIX
# ---------------------------------------------------

if "reviewer_name" not in df.columns:

    df["reviewer_name"] = "Anonymous"

if "likes" not in df.columns:

    df["likes"] = 0

# ---------------------------------------------------
# CATEGORY ENGINE
# ---------------------------------------------------

def categorize_review(text):

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
        "slow",
        "hang"
    ]):

        return "Performance Issues"

    elif any(word in text for word in [
        "kyc",
        "verification",
        "onboarding"
    ]):

        return "KYC/Onboarding"

    elif any(word in text for word in [
        "support",
        "service",
        "response"
    ]):

        return "Customer Support"

    elif any(word in text for word in [
        "great",
        "excellent",
        "smooth",
        "good",
        "amazing"
    ]):

        return "Positive Experience"

    else:

        return "General"

# ---------------------------------------------------
# SENTIMENT
# ---------------------------------------------------

def sentiment_label(rating):

    if rating >= 4:

        return "Positive"

    elif rating == 3:

        return "Neutral"

    else:

        return "Negative"

# ---------------------------------------------------
# APPLY LOGIC
# ---------------------------------------------------

df["Category"] = (
    df["review"]
    .astype(str)
    .apply(categorize_review)
)

df["Sentiment"] = (
    df["rating"]
    .apply(sentiment_label)
)

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("🔍 Filters")

platforms = sorted(
    df["platform"].unique()
)

selected_platform = st.sidebar.selectbox(
    "Choose Platform",
    ["All"] + platforms
)

selected_sentiment = st.sidebar.selectbox(
    "Choose Sentiment",
    ["All", "Positive", "Neutral", "Negative"]
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = df.copy()

if selected_platform != "All":

    filtered_df = filtered_df[
        filtered_df["platform"] == selected_platform
    ]

if selected_sentiment != "All":

    filtered_df = filtered_df[
        filtered_df["Sentiment"] == selected_sentiment
    ]

# ---------------------------------------------------
# SEARCH
# ---------------------------------------------------

search_text = st.text_input(
    "🔎 Search Reviews"
)

if search_text:

    filtered_df = filtered_df[
        filtered_df["review"]
        .str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "📝 Total Reviews",
    len(filtered_df)
)

col2.metric(
    "⭐ Avg Rating",
    round(filtered_df["rating"].mean(), 2)
)

col3.metric(
    "📂 Categories",
    filtered_df["Category"].nunique()
)

# ---------------------------------------------------
# CATEGORY CHART
# ---------------------------------------------------

st.subheader("📊 Review Categories")

category_counts = (
    filtered_df["Category"]
    .value_counts()
    .reset_index()
)

category_counts.columns = [
    "Category",
    "Count"
]

fig = px.bar(
    category_counts,
    x="Category",
    y="Count",
    color="Count",
    text_auto=True,
    title="Complaint & Feedback Categories"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# PLATFORM SUMMARY
# ---------------------------------------------------

st.subheader("🏢 Platform Summary")

platform_summary = (
    filtered_df
    .groupby("platform")
    .agg({
        "rating": ["mean", "count"]
    })
)

platform_summary.columns = [
    "Avg Rating",
    "Total Reviews"
]

platform_summary = (
    platform_summary
    .reset_index()
)

platform_summary["Avg Rating"] = (
    platform_summary["Avg Rating"]
    .round(2)
)

st.dataframe(
    platform_summary,
    use_container_width=True
)

# ---------------------------------------------------
# REVIEW TABLE
# ---------------------------------------------------

st.subheader("📝 Detailed Review Intelligence")

review_table = filtered_df[[
    "platform",
    "reviewer_name",
    "rating",
    "Category",
    "Sentiment",
    "likes",
    "review"
]]

review_table.columns = [
    "Platform",
    "Reviewer",
    "Rating",
    "Category",
    "Sentiment",
    "Likes",
    "Review Comment"
]

st.dataframe(
    review_table,
    use_container_width=True,
    height=700
)
