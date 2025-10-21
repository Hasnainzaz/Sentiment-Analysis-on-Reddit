```markdown
# Reddit Sentiment Full Stack (Streamlit + FastAPI + Docker)

## Features
- User inputs a subreddit name in the Streamlit frontend
- FastAPI backend fetches comments using PRAW and classifies sentiment using VADER
- Docker Compose runs backend and frontend together

## Quick start (Docker)
1. Copy `.env.example` to `.env` and fill in your Reddit API credentials.

2. Build and start:

```bash
docker-compose up --build
```

3. Open the Streamlit frontend at: http://localhost:8501

## Without Docker
### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Set env vars (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
4. `uvicorn app:app --reload --port 8000`

### Frontend
1. `cd frontend`
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

## Notes
- Make sure your Reddit app credentials are correct and the app has access.
- When deploying to cloud, store credentials securely (Secrets manager).