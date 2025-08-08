import os
import csv
import time
import tweepy
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Load environment variables from .env or Render environment
load_dotenv()

# Twitter API keys
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Start a simple Flask server to keep the app awake
app = Flask('')

@app.route('/')
def home():
    return "I'm alive and tweeting!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# Read tweets from CSV
with open("DALLAS.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    tweets = list(reader)

# Loop through all tweets forever
while True:
    for tweet_row in tweets:
        if not tweet_row or not tweet_row[0].strip():
            continue  # Skip empty rows

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

        # Wait 22 minutes before next tweet
        time.sleep(22 * 60)
