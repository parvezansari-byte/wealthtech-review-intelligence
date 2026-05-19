from google_play_scraper import reviews
import pandas as pd
from datetime import datetime
import os

# ---------------------------------------------------
# PLAY STORE APPS
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
# STORAGE
# ---------------------------------------------------

all_reviews = []

# ---------------------------------------------------
# FETCH PLAY STORE REVIEWS
# ---------------------------------------------------

for app_name, app_id in apps.items():

    print(f"Fetching reviews for {app_name}")

    try:

        result, _ = reviews(

            app_id,

            lang="en",

            country="in",

            count=300

        )

        for r in result:

            all_reviews.append({

                "platform":
                    app_name,

                # REAL PLAYSTORE REVIEWER NAME

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
# CREATE DATAFRAME
# ---------------------------------------------------

df = pd.DataFrame(all_reviews)

# ---------------------------------------------------
# CREATE DATA FOLDER
# ---------------------------------------------------

os.makedirs(
    "data",
    exist_ok=True
)

# ---------------------------------------------------
# SAVE CSV
# ---------------------------------------------------

df.to_csv(

    "data/historical_reviews.csv",

    index=False

)

# ---------------------------------------------------
# SUCCESS
# ---------------------------------------------------

print(
    f"Saved {len(df)} real Play Store reviews."
)
