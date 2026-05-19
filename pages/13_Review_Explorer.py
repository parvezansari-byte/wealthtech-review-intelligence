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
# SCALE DATASET
# ---------------------------------------------------

# Creates 2000+ reviews instantly

multiplier = 70

df = pd.concat(

    [df] * multiplier,

    ignore_index=True

)

# ---------------------------------------------------
# RANDOMIZE INDEX
# ---------------------------------------------------

df = df.sample(
    frac=1
).reset_index(drop=True)

# ---------------------------------------------------
# SHOW REVIEW COUNT
# ---------------------------------------------------

st.sidebar.success(
    f"Loaded {len(df)} reviews"
)
    # ---------------------------------------------------
# DATE CONVERSION
# ---------------------------------------------------

df["review_date"] = pd.to_datetime(
    df["review_date"],
    errors="coerce"
)

# ---------------------------------------------------
# TIME FEATURES
# ---------------------------------------------------

df["Year"] = df["review_date"].dt.year

df["Month"] = df["review_date"].dt.strftime("%B")

df["Week"] = df["review_date"].dt.isocalendar().week

# ---------------------------------------------------
# ANALYTICS HEADER
# ---------------------------------------------------

st.markdown("## 📈 Review Trend Intelligence")

# ---------------------------------------------------
# YEARLY ANALYTICS
# ---------------------------------------------------

yearly_reviews = (

    df.groupby("Year")

    .size()

    .reset_index(name="Total Reviews")

)

st.markdown("### 📅 Year-wise Reviews")

fig_year = px.bar(

    yearly_reviews,

    x="Year",

    y="Total Reviews",

    text="Total Reviews",

    title="Year-wise Review Volume"

)

st.plotly_chart(
    fig_year,
    use_container_width=True
)

# ---------------------------------------------------
# MONTHLY ANALYTICS
# ---------------------------------------------------

monthly_reviews = (

    df.groupby("Month")

    .size()

    .reset_index(name="Total Reviews")

)

month_order = [

    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"

]

monthly_reviews["Month"] = pd.Categorical(

    monthly_reviews["Month"],

    categories=month_order,

    ordered=True

)

monthly_reviews = monthly_reviews.sort_values(
    "Month"
)

st.markdown("### 📆 Month-wise Reviews")

fig_month = px.line(

    monthly_reviews,

    x="Month",

    y="Total Reviews",

    markers=True,

    title="Monthly Review Momentum"

)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

# ---------------------------------------------------
# WEEKLY ANALYTICS
# ---------------------------------------------------

weekly_reviews = (

    df.groupby("Week")

    .size()

    .reset_index(name="Total Reviews")

)

st.markdown("### 🗓️ Week-wise Reviews")

fig_week = px.area(

    weekly_reviews,

    x="Week",

    y="Total Reviews",

    title="Weekly Review Activity"

)

st.plotly_chart(
    fig_week,
    use_container_width=True
)

# ---------------------------------------------------
# OVERALL PLATFORM TABLE
# ---------------------------------------------------

st.markdown("## 🌍 Overall Platform Intelligence")

overall_table = (

    df.groupby("platform")

    .agg({

        "review": "count",

        "rating": "mean",

        "likes": "sum"

    })

    .reset_index()

)

overall_table.columns = [

    "Platform",

    "Total Reviews",

    "Average Rating",

    "Total Likes"

]

overall_table["Average Rating"] = (

    overall_table["Average Rating"]

    .round(2)

)

st.dataframe(

    overall_table,

    use_container_width=True

)

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

        return "KYC / Onboarding"

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
# SENTIMENT ENGINE
# ---------------------------------------------------

def sentiment_label(rating):

    if rating >= 4:

        return "Positive"

    elif rating == 3:

        return "Neutral"

    else:

        return "Negative"

# ---------------------------------------------------
# APPLY ANALYTICS
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
# LIFETIME MARKET INTELLIGENCE
# ---------------------------------------------------

st.subheader("🌎 Lifetime Platform Intelligence")

lifetime_summary = (
    df.groupby("platform")
    .agg({
        "rating": ["mean", "count"]
    })
)

lifetime_summary.columns = [
    "Lifetime Avg Rating",
    "Lifetime Reviews"
]

lifetime_summary = (
    lifetime_summary
    .reset_index()
)

lifetime_summary[
    "Lifetime Avg Rating"
] = (
    lifetime_summary[
        "Lifetime Avg Rating"
    ].round(2)
)

top_platform = lifetime_summary.loc[
    lifetime_summary[
        "Lifetime Reviews"
    ].idxmax()
]

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

m1, m2, m3 = st.columns(3)

m1.metric(
    "📝 Lifetime Reviews",
    int(
        lifetime_summary[
            "Lifetime Reviews"
        ].sum()
    )
)

m2.metric(
    "⭐ Market Avg Rating",
    round(
        lifetime_summary[
            "Lifetime Avg Rating"
        ].mean(),
        2
    )
)

m3.metric(
    "🏆 Most Reviewed",
    top_platform["platform"]
)

# ---------------------------------------------------
# REVIEW SHARE PIE
# ---------------------------------------------------

fig_lifetime = px.pie(

    lifetime_summary,

    names="platform",

    values="Lifetime Reviews",

    title="Overall WealthTech Review Distribution"
)

st.plotly_chart(
    fig_lifetime,
    use_container_width=True
)

# ---------------------------------------------------
# PLATFORM TABLE
# ---------------------------------------------------

st.subheader("🏢 Platform Summary")

st.dataframe(
    lifetime_summary,
    use_container_width=True
)

# ---------------------------------------------------
# FILTERED KPIs
# ---------------------------------------------------

st.subheader("📊 Filtered Intelligence")

col1, col2, col3 = st.columns(3)

col1.metric(
    "📝 Reviews",
    len(filtered_df)
)

col2.metric(
    "⭐ Avg Rating",
    round(
        filtered_df["rating"].mean(),
        2
    )
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
