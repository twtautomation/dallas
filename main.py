from flask import Flask
import threading
import csv
import os
import time
import tweepy
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# CSV setup
CSV_FILE = "DALLAS.csv"

# Tweet loop
def tweet_loop():
    print(f"📄 Reading tweets from: {CSV_FILE}")
    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row or not row[0].strip():
                    continue
                text = row[0]
                try:
                    api.update_status(status=text)
                    print(f"✅ Tweeted: {text}")
                except Exception as e:
                    print(f"❌ Error tweeting: {e}")
                time.sleep(21 * 60)  # 21 minutes
    except FileNotFoundError:
        print(f"❌ CSV file '{CSV_FILE}' not found!")

# Flask app for keep-alive
app = Flask(__name__)

@app.route('/')
def index():
    return "🟢 Bot is running (text-only every 21 min)"

# Start tweet loop immediately
threading.Thread(target=tweet_loop).start()

# Start Flask server (for UptimeRobot)
app.run(host='0.0.0.0', port=8080)
