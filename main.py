import os
import csv
import time
import tweepy
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Load environment variables
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate with Twitter API
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Flask app for UptimeRobot pings
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = Thread(target=run)
    thread.start()

# Start Flask server
keep_alive()

# Read tweets from renamed file
csv_filename = "DALLAS.csv"
print(f"📄 Reading tweets from: {csv_filename}")

try:
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        tweets = list(reader)
except FileNotFoundError:
    print(f"❌ File '{csv_filename}' not found!")
    tweets = []

print("🚀 Starting tweet loop...")

# Infinite tweet loop
while True:
    for tweet_row in tweets:
        if not tweet_row or not tweet_row[0].strip():
            continue  # skip empty rows

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
        print("⏱️ Sleeping 22 minutes...\n")
        time.sleep(22 * 60)
