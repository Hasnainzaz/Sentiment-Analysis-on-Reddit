import streamlit as st
import requests
import os

st.set_page_config(page_title="Reddit Sentiment", page_icon="📊")
st.title("📊 Reddit Sentiment Analyzer")

st.markdown("""
Enter a subreddit name (no `r/` prefix) — our service will fetch recent comments and predict whether the subreddit discussion is overall positive, negative, or neutral.
""")

# backend URL (from env or default to localhost)
BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')

subreddit = st.text_input("Subreddit", value="technology")
limit = st.slider("Comments to analyze (max)", 10, 200, 50)

if st.button("Analyze"):
    if subreddit.strip() == "":
        st.error("Please enter a subreddit name.")
    else:
        with st.spinner("Fetching and analyzing..."):
            try:
                resp = requests.get(f"{BACKEND_URL}/analyze/{subreddit}?limit={limit}", timeout=60)
                if resp.status_code == 200:
                    data = resp.json()
                    st.subheader(f"Results for r/{data['subreddit']}")
                    st.metric("Total comments analyzed", data['total_comments'])
                    cols = st.columns(3)
                    cols[0].metric("Positive", data['positive'])
                    cols[1].metric("Negative", data['negative'])
                    cols[2].metric("Neutral", data['neutral'])

                    overall = data['overall_sentiment']
                    if overall == 'positive':
                        st.success(f"Overall sentiment: {overall.upper()} 🎉")
                    elif overall == 'negative':
                        st.error(f"Overall sentiment: {overall.upper()} 😕")
                    else:
                        st.info(f"Overall sentiment: {overall.upper()} 😐")

                else:
                    st.error(f"Backend error: {resp.status_code} - {resp.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")