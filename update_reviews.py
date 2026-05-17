from google_play_scraper import reviews
import pandas as pd
from datetime import datetime
import os

# ---------------------------------------------------
# APPS
# ---------------------------------------------------

apps = {

    "NJ Partner Desk":
        "com.fin.mpartnerdesk",

    "Prudent":
        "com.prumob.mobileapp",

    "AssetPlus":
        "in.assetplus.partner",

    "Wealthy Partner":
        "in.wealthy.android.advisor",

    "Nuvama":
        "com.Edelweiss.FPD.edelweiss_subbroker_app",

    "ZFunds":
        "com.zfunds.experts",

    "FundsIndia Partner":
        "com.fundsindia.partnerapp",

    "Centricity":
        "com.centricity_app",

    "Bonanza":
        "com.bonanzabranch.BranchMbos"
}

# ---------------------------------------------------
# CREATE DATA FOLDER
# ---------------------------------------------------

os.makedirs(
    "data",
    exist_ok=True
)

# ---------------------------------------------------
# LOAD OLD DATA
# ---------------------------------------------------

csv_path = "data/historical_reviews.csv"

if os.path.exists(csv_path):

    old_df = pd.read_csv(csv_path)

else:

    old_df = pd.DataFrame()

# ---------------------------------------------------
# NEW DATA STORAGE
# ---------------------------------------------------

all_reviews = []

# ---------------------------------------------------
# SCRAPE REVIEWS
# ---------------------------------------------------

for app_name, app_id in apps.items():

    print(f"Fetching reviews for {app_name}")

    try:

        result, _ = reviews(

            app_id,

            lang="en",

            country="in",

            count=500

        )

        for r in result:

            all_reviews.append({

                "platform": app_name,

                "reviewer_name":
                    r.get("userName", "Anonymous"),

                "review":
                    r.get("content", ""),

                "rating":
                    r.get("score", 0),

                "likes":
                    r.get("thumbsUpCount", 0),

                "review_date":
                    r.get("at"),

                "scraped_at":
                    datetime.now()

            })

    except Exception as e:

        print(
            f"Error scraping {app_name}: {e}"
        )

# ---------------------------------------------------
# CREATE NEW DATAFRAME
# ---------------------------------------------------

new_df = pd.DataFrame(all_reviews)

# ---------------------------------------------------
# COMBINE OLD + NEW
# ---------------------------------------------------

combined_df = pd.concat(
    [old_df, new_df],
    ignore_index=True
)

# ---------------------------------------------------
# REMOVE DUPLICATES
# ---------------------------------------------------

combined_df = combined_df.drop_duplicates(

    subset=[
        "platform",
        "reviewer_name",
        "review"
    ]
)

# ---------------------------------------------------
# DATE CLEANUP
# ---------------------------------------------------

combined_df["review_date"] = pd.to_datetime(
    combined_df["review_date"],
    errors="coerce"
)

combined_df["scraped_at"] = pd.to_datetime(
    combined_df["scraped_at"],
    errors="coerce"
)

# ---------------------------------------------------
# SAVE CSV
# ---------------------------------------------------

combined_df.to_csv(
    csv_path,
    index=False
)

# ---------------------------------------------------
# SUCCESS
# ---------------------------------------------------

print(
    f"Dataset updated successfully."
)

print(
    f"Total Lifetime Reviews: {len(combined_df)}"
)
