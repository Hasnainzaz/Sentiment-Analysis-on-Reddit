from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from reddit_api import fetch_reddit_comments
from sentiment import analyze_sentiment_batch
import os

app = FastAPI(title="Reddit Sentiment API")

class AnalyzeResponse(BaseModel):
    subreddit: str
    total_comments: int
    positive: int
    negative: int
    neutral: int
    overall_sentiment: str


@app.get("/", tags=["meta"])
def root():
    return {"message": "Reddit Sentiment API is running"}


@app.get("/analyze/{subreddit}", response_model=AnalyzeResponse)
def analyze(subreddit: str, limit: int = 50):
    # simple validation
    if not subreddit or subreddit.strip() == "":
        raise HTTPException(status_code=400, detail="subreddit name required")

    comments = fetch_reddit_comments(subreddit, limit)
    if len(comments) == 0:
        raise HTTPException(status_code=404, detail="no comments found or subreddit not accessible")

    agg = analyze_sentiment_batch(comments)

    positive = agg["positive"]
    negative = agg["negative"]
    neutral = agg["neutral"]

    if positive > negative:
        overall = "positive"
    elif negative > positive:
        overall = "negative"
    else:
        overall = "neutral"

    return {
        "subreddit": subreddit,
        "total_comments": positive + negative + neutral,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "overall_sentiment": overall,
    }