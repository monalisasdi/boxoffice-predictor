import pandas as pd
import requests
import time
import os


# Your TMDB API key
API_KEY = os.getenv("TMDB_API_KEY")

# Load merged dataset
df = pd.read_csv("data/films_merged.csv").head(5000)  # Limit to 5000 movies for testing

# Prepare new columns
tmdb_sentiments = []
tmdb_review_counts = []
tmdb_avg_ratings = []

for index, row in df.iterrows():
    movie_id = row['id']
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={API_KEY}&language=en-US&page=1"

    try:
        response = requests.get(url)
        data = response.json()
        reviews = data.get("results", [])

        print(f"\n Raw TMDB result for ID {movie_id}: {len(data.get('results', []))} reviews found.")

        sentiment_scores = []
        ratings = []

        for review in reviews:
            content = review.get("content", "")
            if content and len(content) > 20:
                polarity = TextBlob(content).sentiment.polarity
                sentiment_scores.append(polarity)

            rating = review.get("author_details", {}).get("rating")
            if rating is not None:
                ratings.append(rating)

        # Compute averages while excluding missing values
        avg_sentiment = round(sum(sentiment_scores) / len(sentiment_scores), 3) if sentiment_scores else None
        avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else None

        tmdb_sentiments.append(avg_sentiment)
        tmdb_avg_ratings.append(avg_rating)
        tmdb_review_counts.append(len(reviews))

    except Exception as e:
        print(f"Error for movie ID {movie_id}: {e}")
        tmdb_sentiments.append(None)
        tmdb_avg_ratings.append(None)
        tmdb_review_counts.append(0)

    time.sleep(0.3)  # Respect TMDB API rate limits

# ➕ Add new columns to the DataFrame
df['tmdb_sentiment_score'] = tmdb_sentiments
df['tmdb_avg_rating'] = tmdb_avg_ratings
df['tmdb_review_count'] = tmdb_review_counts

# 💾 Save enriched dataset
df.to_csv("data/films_with_tmdb.csv", index=False)
print("✅ TMDB data successfully added: data/films_with_tmdb.csv")
