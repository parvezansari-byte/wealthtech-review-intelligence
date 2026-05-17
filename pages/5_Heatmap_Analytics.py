import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Heatmap Analytics",
    layout="wide"
)

st.title("🔥 WealthTech Maturity Heatmap")

st.markdown("""
Institutional benchmarking of India’s leading wealth-tech platforms.
""")

# -----------------------------------
# HEATMAP DATA
# -----------------------------------

heatmap_data = pd.DataFrame({

    "UI/UX": [
        6,
        7,
        9,
        9,
        7,
        8,
        8,
        7,
        6,
        9,
        9,
        8
    ],

    "Automation": [
        6,
        7,
        9,
        9,
        7,
        7,
        8,
        7,
        6,
        8,
        9,
        8
    ],

    "Advisor Experience": [
        8,
        8,
        9,
        9,
        8,
        8,
        8,
        8,
        7,
        7,
        7,
        7
    ],

    "Stability": [
        6,
        7,
        8,
        8,
        7,
        7,
        7,
        7,
        6,
        8,
        9,
        8
    ],

    "Innovation": [
        5,
        6,
        9,
        9,
        7,
        7,
        7,
        7,
        5,
        9,
        9,
        8
    ]

},

index=[

    "NJ Partner Desk",
    "Prudent",
    "AssetPlus",
    "Wealthy Partner",
    "Nuvama",
    "ZFunds Experts",
    "FundsIndia Partner",
    "Centricity",
    "Bonanza",
    "Groww",
    "Zerodha",
    "Upstox"

])

# -----------------------------------
# HEATMAP
# -----------------------------------

fig, ax = plt.subplots(figsize=(14, 8))

sns.heatmap(
    heatmap_data,
    annot=True,
    cmap="RdYlGn",
    linewidths=0.5,
    ax=ax
)

st.pyplot(fig)

# -----------------------------------
# INSIGHTS
# -----------------------------------

st.subheader("🧠 Strategic Insights")

st.info("""

### Key Market Observations

✅ Modern advisor operating systems like AssetPlus and Wealthy score highest on innovation and UX.

✅ Traditional distribution platforms retain strong advisor ecosystem depth but lag in UI modernization.

✅ Retail fintech leaders like Zerodha and Groww dominate digital experience and platform stability.

✅ Enterprise platforms like Nuvama maintain strong operational capabilities but face workflow complexity challenges.

✅ The market is rapidly shifting toward:
- AI-enabled workflows
- mobile-first advisory
- automation-led engagement
- intelligent onboarding systems

""")

# -----------------------------------
# MARKET SEGMENTS
# -----------------------------------

st.subheader("📊 Platform Segmentation")

segment_df = pd.DataFrame({

    "Segment": [
        "Traditional Distribution Infra",
        "Modern Advisor Operating Systems",
        "Enterprise Wealth Platforms",
        "Retail Fintech Leaders",
        "Digital Investment Platforms"
    ],

    "Platforms": [
        "NJ, Prudent, Bonanza",
        "AssetPlus, Wealthy",
        "Nuvama",
        "Groww, Zerodha, Upstox",
        "FundsIndia, ZFunds"
    ]

})

st.dataframe(
    segment_df,
    use_container_width=True
)
