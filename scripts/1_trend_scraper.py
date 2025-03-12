import praw
import json
import random
import os
import time
import requests
from googleapiclient.discovery import build

# Ensure the script always finds config.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# Load configuration
with open(CONFIG_PATH) as f:
    config = json.load(f)

TOPICS_FILE = os.path.join(BASE_DIR, "inputs", "topics.txt")
DELETE_AFTER_DAYS = 3  # Auto-delete topics older than X days


def get_reddit_trends():
    """Fetch top trending topics from Reddit."""
    reddit = praw.Reddit(
        client_id=config['reddit']['client_id'],
        client_secret=config['reddit']['client_secret'],
        user_agent="AutoMindStudio/1.0"
    )
    
    top_topics = [
        submission.title for submission in reddit.subreddit('movies').hot(limit=10)
    ]
    return top_topics


def get_google_trends():
    """Fetch top trending topics from Google Trends."""
    api_key = config['google']['api_key']
    cse_id = config['google']['cse_id']
    
    url = f"https://www.googleapis.com/customsearch/v1?q=trending&cx={cse_id}&key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return [item['title'] for item in data.get('items', [])]
    return []


def save_topics(topics):
    """Save topics to file with timestamps."""
    with open(TOPICS_FILE, "a") as f:
        for topic in topics:
            f.write(f"{time.time()}|{topic}\n")


def clean_old_topics():
    """Remove topics older than DELETE_AFTER_DAYS."""
    if not os.path.exists(TOPICS_FILE):
        return
    
    cutoff_time = time.time() - (DELETE_AFTER_DAYS * 86400)
    new_lines = []
    
    with open(TOPICS_FILE, "r") as f:
        for line in f:
            timestamp, topic = line.strip().split("|", 1)
            if float(timestamp) > cutoff_time:
                new_lines.append(line)
    
    with open(TOPICS_FILE, "w") as f:
        f.writelines(new_lines)


if __name__ == "__main__":
    print("🔍 Fetching trending topics...")

    reddit_trends = get_reddit_trends()
    google_trends = get_google_trends()

    all_trends = list(set(reddit_trends + google_trends))  # Remove duplicates
    random.shuffle(all_trends)  # Shuffle for randomness

    print(f"✅ {len(all_trends)} trending topics found!")

    save_topics(all_trends)
    clean_old_topics()

    print("📂 Topics saved and old ones removed!")

