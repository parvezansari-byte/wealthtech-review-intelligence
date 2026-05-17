import pandas as pd
from datetime import datetime
from google_play_scraper import reviews, Sort

# -----------------------------------
# APPS
# -----------------------------------

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
            count=200
        )

        for r in result:

            all_reviews.append({
                "platform": app_name,
                "review": r.get("content", ""),
                "rating": r.get("score", 0),
                "review_date": r.get("at", ""),
                "scraped_at": datetime.now()
            })

        print(f"SUCCESS: {app_name}")

    except Exception as e:

        print(f"ERROR: {app_name} -> {e}")

# -----------------------------------
# SAVE DATA
# -----------------------------------

reviews_df = pd.DataFrame(all_reviews)

reviews_df.to_csv(
    "data/latest_reviews.csv",
    index=False
)

print("Review update completed.")
