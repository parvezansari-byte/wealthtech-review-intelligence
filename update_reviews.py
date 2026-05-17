import pandas as pd

from datetime import datetime

from google_play_scraper import reviews, Sort

# -----------------------------------
# APPS
# -----------------------------------

apps = {

    "Groww": "com.nextbillion.groww",

    "Angel One": "com.msf.angelmobile",

    "Zerodha": "com.zerodha.kite3",

    "Upstox": "in.upstox.pro",

    "Wealthy Partner": "in.wealthy.android.advisor",

    "Prudent": "com.prumob.mobileapp",

    "AssetPlus": "in.assetplus.partner"
}

# -----------------------------------
# STORAGE
# -----------------------------------

all_reviews = []

# -----------------------------------
# FETCH REVIEWS
# -----------------------------------

for app_name, app_id in apps.items():

    try:

        result, _ = reviews(
            app_id,
            lang="en",
            country="in",
            sort=Sort.NEWEST,
            count=100
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

# -----------------------------------
# CREATE DATAFRAME
# -----------------------------------

reviews_df = pd.DataFrame(all_reviews)

# -----------------------------------
# CHECK EMPTY
# -----------------------------------

if reviews_df.empty:

    print("No reviews fetched.")

else:

    # SAVE CSV
    reviews_df.to_csv(
        "data/latest_reviews.csv",
        index=False
    )

    print("CSV saved successfully.")
