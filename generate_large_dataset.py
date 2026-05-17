import pandas as pd
import random
from datetime import datetime, timedelta

# ---------------------------------------------------
# PLATFORMS
# ---------------------------------------------------

platforms = [

    "Prudent",

    "NJ Partner Desk",

    "AssetPlus",

    "Wealthy Partner",

    "Nuvama",

    "ZFunds",

    "FundsIndia Partner",

    "Centricity",

    "Bonanza"
]

# ---------------------------------------------------
# REVIEW COMMENTS
# ---------------------------------------------------

positive_reviews = [

    "Excellent onboarding experience",

    "Very smooth advisor workflow",

    "Great investment platform",

    "Amazing app for MFD business",

    "Fast and reliable platform",

    "Excellent UI and usability",

    "Very useful for advisors",

    "Easy SIP management",

    "Best WealthTech platform"

]

negative_reviews = [

    "App crashes frequently",

    "Login issue happens often",

    "Slow performance",

    "KYC process is difficult",

    "Customer support is poor",

    "OTP verification problem",

    "App hangs sometimes",

    "Needs UI improvement",

    "Technical glitches occur"

]

neutral_reviews = [

    "Average experience overall",

    "Features are decent",

    "Can improve performance",

    "UI is acceptable",

    "Moderate experience",

    "Works fine mostly"

]

# ---------------------------------------------------
# NAMES
# ---------------------------------------------------

names = [

    "Rahul",
    "Amit",
    "Sneha",
    "Priya",
    "Arjun",
    "Vikas",
    "Karan",
    "Anjali",
    "Rohit",
    "Meera"
]

# ---------------------------------------------------
# DATA STORAGE
# ---------------------------------------------------

rows = []

# ---------------------------------------------------
# GENERATE 2000 REVIEWS
# ---------------------------------------------------

for i in range(2000):

    platform = random.choice(platforms)

    sentiment = random.choice([
        "positive",
        "positive",
        "positive",
        "neutral",
        "negative"
    ])

    if sentiment == "positive":

        review = random.choice(
            positive_reviews
        )

        rating = random.choice([4, 5])

    elif sentiment == "negative":

        review = random.choice(
            negative_reviews
        )

        rating = random.choice([1, 2])

    else:

        review = random.choice(
            neutral_reviews
        )

        rating = 3

    random_days = random.randint(0, 180)

    review_date = (
        datetime.now()
        - timedelta(days=random_days)
    )

    rows.append({

        "platform":
            platform,

        "reviewer_name":
            random.choice(names),

        "review":
            review,

        "rating":
            rating,

        "likes":
            random.randint(0, 25),

        "review_date":
            review_date,

        "scraped_at":
            datetime.now()

    })

# ---------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------

df = pd.DataFrame(rows)

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
    f"Generated {len(df)} reviews successfully."
)
