from google_play_scraper import reviews, Sort
import pandas as pd

def fetch_reviews(app_id, count=100):

    try:

        result, continuation_token = reviews(
            app_id,
            lang="en",
            country="in",
            sort=Sort.NEWEST,
            count=count
        )

        if not result:
            return pd.DataFrame()

        data = []

        for r in result:

            data.append({
                "review": r.get("content", ""),
                "rating": r.get("score", 0),
                "date": r.get("at", "")
            })

        df = pd.DataFrame(data)

        return df

    except Exception as e:

        print("SCRAPER ERROR:", e)

        return pd.DataFrame()
