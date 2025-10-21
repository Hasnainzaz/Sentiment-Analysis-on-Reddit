from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List, Dict

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> Dict:
    """Return sentiment dict for a single text."""
    vs = analyzer.polarity_scores(text)
    # compound polarity ranges [-1, 1]
    compound = vs.get('compound', 0.0)
    if compound >= 0.05:
        sentiment = 'positive'
    elif compound <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    return {"text": text, "compound": compound, "sentiment": sentiment}


def analyze_sentiment_batch(texts: List[str]) -> Dict[str, int]:
    positive = negative = neutral = 0
    for t in texts:
        r = analyze_sentiment(t)
        if r['sentiment'] == 'positive':
            positive += 1
        elif r['sentiment'] == 'negative':
            negative += 1
        else:
            neutral += 1
    return {"positive": positive, "negative": negative, "neutral": neutral}
