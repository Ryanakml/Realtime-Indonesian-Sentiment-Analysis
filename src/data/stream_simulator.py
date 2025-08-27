# src/data/stream_simulator.py
import snscrape.modules.twitter as sntwitter
import praw
import json
import time
import os
import argparse
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

def simulate_twitter_stream(producer, topic, query, limit=100):
    """Simulasikan aliran data dari Twitter menggunakan snscrape."""
    scraper = sntwitter.TwitterSearchScraper(query)
    print(f"Memulai streaming Twitter untuk query: '{query}'")
    for i, tweet in enumerate(scraper.get_items()):
        if i >= limit:
            break
        tweet_data = {
            "id": tweet.id,
            "text": tweet.rawContent,
            "source": "twitter",
            "timestamp_ms": int(tweet.date.timestamp() * 1000),
            "user": {"id": tweet.user.id, "followers_count": tweet.user.followersCount},
        }
        producer.send(topic, value=json.dumps(tweet_data).encode('utf-8'))
        print(f"Mengirim tweet: {tweet.id}")
        time.sleep(2) # Tiru jeda antar-tweet

def simulate_reddit_stream(producer, topic, subreddit_name, limit=100):
    """Simulasikan aliran data dari Reddit menggunakan PRAW."""
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )
    subreddit = reddit.subreddit(subreddit_name)
    print(f"Memulai streaming Reddit untuk subreddit: 'r/{subreddit_name}'")
    for i, comment in enumerate(subreddit.stream.comments(skip_existing=True)):
        if i >= limit:
            break
        comment_data = {
            "id": comment.id,
            "text": comment.body,
            "source": "reddit",
            "timestamp_ms": int(comment.created_utc * 1000),
            "user": {"id": str(comment.author.id) if comment.author else "deleted"},
        }
        producer.send(topic, value=json.dumps(comment_data).encode('utf-8'))
        print(f"Mengirim komentar Reddit: {comment.id}")
        time.sleep(2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulasi aliran data media sosial ke Kafka.")
    parser.add_argument("--source", type=str, required=True, choices=["twitter", "reddit"], help="Sumber data (twitter atau reddit)")
    args = parser.parse_args()

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    topic_name = "social_media_stream"

    if args.source == "twitter":
        # Query untuk topik yang relevan di Indonesia
        twitter_query = "(gofood OR tokopedia OR shopee) lang:id"
        simulate_twitter_stream(producer, topic_name, twitter_query)
    elif args.source == "reddit":
        simulate_reddit_stream(producer, topic_name, "indonesia")