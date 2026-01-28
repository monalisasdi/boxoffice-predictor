import praw
import pandas as pd
import time
import os

# Reddit authentication
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Read movies dataset
films = pd.read_csv("data/films_100000.csv").head(10000)

# Store results
results = []

for index, row in films.iterrows():
    title = row['title']
    query = f"{title} movie"
    subreddit = reddit.subreddit("movies")

    print(f"\n🔎 Movie: {title}")

    sentiments = []
    upvotes = []
    volume = 0
    valid_texts = []

    try:
        for post in subreddit.search(query, limit=30):
            texte = (post.title or "") + " " + (post.selftext or "")
            texte = texte.strip().lower()

            # 🧹 Basic filtering
            if title.lower() not in post.title.lower():
                continue
            if len(texte) < 20:
                continue
            if any(word in texte for word in ["trailer", "poster", "oscars", "grammy"]):
                continue

            opinion_keywords = [
                "i loved", "i hated", "i liked", "i disliked", "i enjoyed", "i didn't like",
                "amazing", "boring", "overrated", "underrated", "masterpiece", "awful",
                "incredible", "terrible", "fantastic", "phenomenal", "disappointing",
                "so bad", "so good", "pretty good", "very bad", "absolute trash", "pure gold",
                "blew my mind", "broke my heart", "made me cry", "i was shocked",
                "waste of time", "worth watching", "too long", "too slow", "too short",
                "emotional", "predictable", "surprising", "better than expected",
                "not as good as", "one of the best", "one of the worst", "best movie ever",
                "worst movie ever", "my favorite film", "couldn’t finish it", "slept through it"
            ]

            # Keep only opinion-based posts
            if not any(word in texte for word in opinion_keywords):
                continue

            # Accepted post → Sentiment analysis + data collection
            sentiment = TextBlob(texte).sentiment.polarity
            sentiments.append(sentiment)
            upvotes.append(post.score)
            valid_texts.append(texte)
            volume += 1

            time.sleep(0.2)  # Respect Reddit API rate limits

    except Exception as e:
        print(f"Error for {title}: {e}")
        continue

    # Compute averages
    sentiment_avg = sum(sentiments) / len(sentiments) if sentiments else 0
    upvotes_avg = sum(upvotes) / len(upvotes) if upvotes else 0

    results.append({
        "title": title,
        "reddit_volume": volume,
        "sentiment_score": round(sentiment_avg, 3),
        "avg_upvotes": round(upvotes_avg, 1),
        "reddit_texts": " ||| ".join(valid_texts)
    })

# Final export
df_results = pd.DataFrame(results)
df_results.to_csv("data/films_with_reddit.csv", index=False)
print("\n Reddit enrichment completed: data/films_with_reddit.csv")
