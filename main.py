import tweepy
import os
import csv
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv(ATGU86POelB8h7huUkqC0d8Sy)
API_SECRET = os.getenv(jmCm1dsNEVL0917CDEBrhYul93tJCohefONwqhtcTc5R9G2nL1)
ACCESS_TOKEN = os.getenv(1950301888013819905-O2qkqjyp9WZt2yK08TpEHLxdYtNBx6)
ACCESS_SECRET = os.getenv(U378Mt757NjO4ds4rMDwwlDVRSgyQMJOZjbOTMrv5BfAL)

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

with open(DALLAS.csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    tweets = list(reader)

while True:
    for tweet_row in tweets:
        if not tweet_row:
            continue

        text = tweet_row[0].strip()
        image_file = tweet_row[1].strip() if len(tweet_row) > 1 else None

        try:
            if image_file and os.path.exists(image_file):
                media = api.media_upload(image_file)
                api.update_status(status=text, media_ids=[media.media_id])
                print(f"✅ Tweeted with image: {text}")
            else:
                api.update_status(status=text)
                print(f"✅ Tweeted (text only): {text}")
        except Exception as e:
            print(f"❌ Error tweeting: {e}")

        time.sleep(22 * 60)  # Wait 29 minutes before the next tweet
