import streamlit as st
    title="Review Categories"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# PLATFORM REVIEW SUMMARY
# ---------------------------------------------------

st.subheader("🏢 Platform Review Summary")

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
