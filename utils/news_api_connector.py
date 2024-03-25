import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))
sys.path.append(os.path.dirname(__file__))
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from datetime import datetime
import json
from config.application_config import ApplicationConfig
import time
import file_utils

# Assuming these are your category endpoints or functions that fetch data
CATEGORIES = [ 
    "business", "technology", "entertainment", "science", "sports", "health"
]

api_key = ApplicationConfig.NEWS_API_KEY

# Base URL for fetching news articles; replace with your actual base URL
BASE_URL = "http://newsapi.org/v2/top-headlines?category={category}&apiKey={api_key}&language=en"


# Construct the path to articles.jsonl relative to the current script

def fetch_articles_for_category(category):
    """
    Fetches articles from the API for a given category.
    """
    url = BASE_URL.format(category=category, api_key=api_key)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        print(f"Error fetching articles for category {category}: {response.status_code}")
        return []

def save_articles(articles):
    """
    Saves articles to a JSONL file, appending new articles.
    Each line in the file is a separate JSON object.
    """
    JSON_FILE_PATH = file_utils.get_path(ApplicationConfig.DATA_DIR, "articles.jsonl")
    with open(JSON_FILE_PATH, 'a', encoding='utf-8') as file:
        for article in articles:
            json_line = json.dumps(article, ensure_ascii=False)
            file.write(json_line + '\n')

def fetch_and_save_all_articles():
    new_articles = []
    for category in CATEGORIES:
        articles = fetch_articles_for_category(category)
        for article in articles:
            # Simplified structure; adjust as needed
            print(articles)
            new_article = {
                "summary": article.get('description', ''),
                "title": article.get('title', '')
            }
            new_articles.append(new_article)
    
    if new_articles:
        save_articles(new_articles)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # RUns every 2 min of each hour
    scheduler.add_job(fetch_and_save_all_articles, 'cron', minute='*/5')
    # fetch_and_save_all_articles()
    try:
        print("Starting scheduler. Press Ctrl+C to exit.")
        scheduler.start()  # This will block the main thread
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Exiting the script...")
        scheduler.shutdown()  # Cleanly shutdown the scheduler before exiting
