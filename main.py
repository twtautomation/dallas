from flask import Flask
import threading
import csv
import os
import time
import tweepy
from dotenv import load_dotenv

load_dotenv()

# Twitter API keys from .env
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Auth
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# CSV and image folder settings
CSV_FILE = "DALLAS.csv"
IMAGE_FOLDER = "."

def tweet_loop():
    print(f"📄 Reading tweets from: {CSV_FILE}")
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:
                continue
            text = row[0]
            image_file = row[1] if len(row) > 1 else ""

            try:
                if image_file:
                    image_path = os.path.join(IMAGE_FOLDER, image_file)
                    if os.path.exists(image_path):
                        media = api.media_upload(image_path)
                        api.update_status(status=text, media_ids=[media.media_id])
                        print(f"✅ Tweeted with image: {text}")
                    else:
                        print(f"⚠️ Image not found: {image_path}")
                        api.update_status(status=text)
                        print(f"✅ Tweeted (text only fallback): {text}")
                else:
                    api.update_status(status=text)
                    print(f"✅ Tweeted (text only): {text}")

            except Exception as e:
                print(f"❌ Error tweeting: {e}")

            time.sleep(2 * 60)  # Wait 2 minutes before the next tweet

# Flask app just to stay alive
app = Flask(__name__)

@app.route('/')
def index():
    return "🟢 Twitter bot is running."

# Background thread
def start_bot():
    print("🚀 Starting tweet loop...")
    tweet_loop()

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()
    app.run(host='0.0.0.0', port=8080)
