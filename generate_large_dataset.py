import pandas as pd
import random
from datetime import datetime, timedelta

# ---------------------------------------------------
# SETTINGS
# ---------------------------------------------------

TOTAL_REVIEWS = 5000

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

positive_reviews = [

    "Excellent onboarding experience",
    "Smooth investment journey",
    "Amazing advisor platform",
    "Best wealth management app",
    "Easy SIP process",
    "Very useful dashboard",
    "Fast and reliable app",
    "Great UI and workflow"

]

negative_reviews = [

    "Login issue occurs",
    "App crashes frequently",
    "Slow performance",
    "KYC issue happens",
    "Poor customer support",
    "OTP verification problem",
    "Technical glitches found"

]

neutral_reviews = [

    "Average platform experience",
    "Features are decent",
    "Can improve UI",
    "Moderate usability",
    "Good but needs updates"

]

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
    "Meera",
    "Divya",
    "Pooja",
    "Simran",
    "Sachin",
    "Ravi"

]

# ---------------------------------------------------
# GENERATE DATA
# ---------------------------------------------------

rows = []

for i in range(TOTAL_REVIEWS):

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

    random_days = random.randint(0, 365)

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
            random.randint(0, 50),

        "review_date":
            review_date,

        "scraped_at":
            datetime.now()

    })

# ---------------------------------------------------
# DATAFRAME
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

    f"{len(df)} reviews generated successfully."

)
