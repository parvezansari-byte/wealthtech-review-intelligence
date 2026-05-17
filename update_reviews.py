import os
import pandas as pd

from datetime import datetime

from google_play_scraper import reviews, Sort

# ---------------------------------------------------
# CREATE FOLDERS
# ---------------------------------------------------

os.makedirs("data/daily", exist_ok=True)

os.makedirs("data/monthly", exist_ok=True)

# ---------------------------------------------------
# DATE VARIABLES
# ---------------------------------------------------

today = datetime.now()

daily_file = today.strftime(
    "data/daily/reviews_%Y_%m_%d.csv"
)

monthly_file = today.strftime(
    "data/monthly/reviews_%Y_%m.csv"
)

# ---------------------------------------------------
# APPS
# ---------------------------------------------------

apps = {

    "NJ Partner Desk": "com.fin.mpartnerdesk",

    "Prudent": "com.prumob.mobileapp",

    "AssetPlus": "in.assetplus.partner",

    "Wealthy Partner": "in.wealthy.android.advisor",

    "Nuvama": "com.Edelweiss.FPD.edelweiss_subbroker_app",

    "ZFunds Experts": "com.zfunds.experts",

    "FundsIndia Partner": "com.fundsindia.partnerapp",

    "Centricity": "com.centricity_app",

    "Bonanza": "com.bonanzabranch.BranchMbos",

    "Groww": "com.nextbillion.groww",

    "Angel One": "com.msf.angelmobile",

    "Zerodha": "com.zerodha.kite3",

    "Upstox": "in.upstox.pro"
}

# ---------------------------------------------------
# STORAGE
# ---------------------------------------------------

all_reviews = []

# ---------------------------------------------------
# FETCH REVIEWS
# ---------------------------------------------------

for app_name, app_id in apps.items():

    try:

        result, _ = reviews(
            app_id,
            lang="en",
            country="in",
            sort=Sort.NEWEST,
            count=200
        )

        print(f"{app_name}: {len(result)} reviews fetched")

        for r in result:

            all_reviews.append({

                "platform": app_name,

                "review": r.get("content", ""),

                "rating": r.get("score", 0),

                "review_date": r.get("at", ""),

                "scraped_at": datetime.now()

            })

    except Exception as e:

        print(f"ERROR in {app_name}: {e}")

# ---------------------------------------------------
# DATAFRAME
# ---------------------------------------------------

reviews_df = pd.DataFrame(all_reviews)

# ---------------------------------------------------
# EMPTY CHECK
# ---------------------------------------------------

if reviews_df.empty:

    print("No reviews fetched.")

else:

    # ---------------------------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------------------------

    reviews_df = reviews_df.drop_duplicates(
        subset=["platform", "review"]
    )

    # ---------------------------------------------------
    # SAVE LATEST
    # ---------------------------------------------------

    reviews_df.to_csv(
        "data/latest_reviews.csv",
        index=False
    )

    # ---------------------------------------------------
    # DAILY SNAPSHOT
    # ---------------------------------------------------

    reviews_df.to_csv(
        daily_file,
        index=False
    )

    # ---------------------------------------------------
    # MONTHLY SNAPSHOT
    # ---------------------------------------------------

    reviews_df.to_csv(
        monthly_file,
        index=False
    )

    # ---------------------------------------------------
    # HISTORICAL DATABASE
    # ---------------------------------------------------

    historical_path = (
        "data/historical_reviews.csv"
    )

    if os.path.exists(historical_path):

        historical_df = pd.read_csv(
            historical_path
        )

        combined_df = pd.concat([
            historical_df,
            reviews_df
        ])

        combined_df = combined_df.drop_duplicates(
            subset=["platform", "review"]
        )

    else:

        combined_df = reviews_df

    combined_df.to_csv(
        historical_path,
        index=False
    )

    # ---------------------------------------------------
    # STATUS
    # ---------------------------------------------------

    print("Latest reviews updated.")

    print("Daily snapshot created.")

    print("Monthly snapshot created.")

    print("Historical database updated.")
