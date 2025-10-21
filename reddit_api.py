# backend/reddit_api.py
from pathlib import Path
from dotenv import load_dotenv
import os
from typing import List
import praw

# load .env from repo root (one level up from backend/)
ROOT = Path(__file__).resolve().parents[1]   # repo root
env_path = ROOT / ".env"
load_dotenv(env_path)  # now os.environ will contain values from .env

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT", "reddit-sentiment-app")

def _reddit():
    return praw.Reddit(client_id=CLIENT_ID,
                       client_secret=CLIENT_SECRET,
                       user_agent=USER_AGENT)

def fetch_reddit_comments(subreddit_name: str, limit: int = 50) -> List[str]:
    r = _reddit()
    comments = []
    try:
        subreddit = r.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=limit):
            submission.comments.replace_more(limit=0)
            for c in submission.comments.list():
                if hasattr(c, 'body') and c.body:
                    comments.append(c.body)
                if len(comments) >= limit:
                    break
            if len(comments) >= limit:
                break
    except Exception as e:
        print("Error fetching from Reddit:", e)
        return []
    return comments
# somewhere after load_dotenv and CLIENT_ID assignment
print("Loaded REDDIT_CLIENT_ID present?:", bool(CLIENT_ID))

