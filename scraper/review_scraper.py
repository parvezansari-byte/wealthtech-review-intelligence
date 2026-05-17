from google_play_scraper import reviews, Sort
import pandas as pd

def fetch_reviews(app_id, count=100):

    result, _ = reviews(
        app_id,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=count
    )

    data = []

    for r in result:
        data.append({
            "review": r['content'],
            "rating": r['score'],
            "date": r['at']
        })

    return pd.DataFrame(data)
