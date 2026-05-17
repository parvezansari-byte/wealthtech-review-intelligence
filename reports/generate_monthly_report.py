import os

import pandas as pd

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

# ---------------------------------------------------
# CREATE REPORT FOLDER
# ---------------------------------------------------

os.makedirs(
    "reports",
    exist_ok=True
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv(
    "data/historical_reviews.csv"
)

# ---------------------------------------------------
# SUMMARY
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
# REPORT NAME
# ---------------------------------------------------

today = datetime.now()

report_name = today.strftime(
    "reports/WealthTech_Report_%Y_%m.pdf"
)

# ---------------------------------------------------
# PDF SETUP
# ---------------------------------------------------

doc = SimpleDocTemplate(
    report_name
)

styles = getSampleStyleSheet()

elements = []

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

title = Paragraph(

    "WealthTech Intelligence Report",

    styles["Title"]

)

elements.append(title)

elements.append(
    Spacer(1, 12)
)

# ---------------------------------------------------
# MARKET SUMMARY
# ---------------------------------------------------

market_avg = round(
    summary["Avg Rating"].mean(),
    2
)

top_platform = summary.loc[
    summary["Avg Rating"].idxmax()
]

market_text = f"""
<b>Market Overview</b><br/><br/>

Average Market Rating:
{market_avg}<br/><br/>

Top Platform:
{top_platform['Platform']}<br/><br/>

The WealthTech ecosystem continues shifting toward:
- mobile-first advisory
- automation-led workflows
- intelligent onboarding
- advisor operating systems
"""

elements.append(
    Paragraph(
        market_text,
        styles["BodyText"]
    )
)

elements.append(
    Spacer(1, 12)
)

# ---------------------------------------------------
# PLATFORM DETAILS
# ---------------------------------------------------

for _, row in summary.iterrows():

    text = f"""
<b>{row['Platform']}</b><br/>

Average Rating:
{round(row['Avg Rating'],2)}<br/>

Total Reviews:
{row['Total Reviews']}<br/><br/>
"""

    elements.append(
        Paragraph(
            text,
            styles["BodyText"]
        )
    )

# ---------------------------------------------------
# BUILD PDF
# ---------------------------------------------------

doc.build(elements)

print(
    f"Monthly report generated: {report_name}"
)
