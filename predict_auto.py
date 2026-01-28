import requests
import pandas as pd
from textblob import TextBlob
import praw
import joblib
import time

#  API keys
TMDB_API_KEY = "f2bfff5ffbc0fd3443dec7bf64943e10"
reddit = praw.Reddit(
    client_id="MOR2kDcCeFvf0ZGC1-i8Yg",
    client_secret="4tr3seufYxScsdkN4qN8S9nUfINV5g",
    user_agent="boxoffice script by u/Effective_Science_41"
)

#  API functions
def chercher_film_tmdb(titre):
    url = f"https://api.themoviedb.org/3/search/movie?query={titre}&api_key={TMDB_API_KEY}&language=en-US"
    r = requests.get(url)
    data = r.json()
    if data['results']:
        film = data['results'][0]
        return film['id'], film['title']
    return None, None

def get_film_details_tmdb(film_id):
    url = f"https://api.themoviedb.org/3/movie/{film_id}?api_key={TMDB_API_KEY}&language=en-US"
    return requests.get(url).json()

def get_tmdb_reviews(film_id):
    url = f"https://api.themoviedb.org/3/movie/{film_id}/reviews?api_key={TMDB_API_KEY}&language=en-US&page=1"
    data = requests.get(url).json()
    sentiments, ratings = [], []
    for review in data.get('results', []):
        texte = review.get("content", "")
        note = review.get("author_details", {}).get("rating")
        if texte:
            sentiments.append(TextBlob(texte).sentiment.polarity)
        if note is not None:
            ratings.append(note)
    return (
        round(sum(sentiments) / len(sentiments), 3) if sentiments else 0,
        round(sum(ratings) / len(ratings), 1) if ratings else 0,
        len(data.get('results', []))
    )

def get_reddit_data(film_title, max_posts=30):
    subreddit = reddit.subreddit("movies")
    query = f"{film_title} movie"
    sentiments, upvotes = [], []
    volume = 0
    opinion_keywords = [
        "i loved", "i hated", "i liked", "i disliked", "i enjoyed", "i didn't like",
        "amazing", "boring", "overrated", "underrated", "masterpiece", "awful", "incredible",
        "terrible", "fantastic", "phenomenal", "disappointing", "so bad", "so good", "pretty good",
        "very bad", "absolute trash", "pure gold", "blew my mind", "broke my heart", "made me cry",
        "i was shocked", "waste of time", "worth watching", "too long", "too slow", "too short",
        "emotional", "predictable", "surprising", "better than expected", "not as good as",
        "one of the best", "one of the worst", "best movie ever", "worst movie ever",
        "my favorite film", "couldn’t finish it", "slept through it",
    ]
    try:
        for post in subreddit.search(query, limit=max_posts):
            texte = (post.title or "") + " " + (post.selftext or "")
            texte = texte.strip().lower()
            if len(texte) < 20 or "trailer" in texte or "poster" in texte:
                continue
            if not any(word in texte for word in opinion_keywords):
                continue
            sentiments.append(TextBlob(texte).sentiment.polarity)
            upvotes.append(post.score)
            volume += 1
            time.sleep(0.2)
    except Exception as e:
        print(f"❌ Reddit error: {e}")
    return (
        round(sum(sentiments) / len(sentiments), 3) if sentiments else 0,
        round(sum(upvotes) / len(upvotes), 1) if upvotes else 0,
        volume
    )

#  Script execution
if __name__ == "__main__":
    titre_film = input(" Enter the movie title: ")
    film_id, titre_officiel = chercher_film_tmdb(titre_film)

    if film_id:
        print(f" Movie found: {titre_officiel} (ID: {film_id})")
        details = get_film_details_tmdb(film_id)
        tmdb_sentiment, tmdb_rating, tmdb_count = get_tmdb_reviews(film_id)
        reddit_sentiment, reddit_upvotes, reddit_volume = get_reddit_data(titre_officiel)

        data_film = {
            "popularity": details.get("popularity", 0),
            "budget": details.get("budget", 0),
            "revenue": details.get("revenue", 0),
            "runtime": details.get("runtime", 0),
            "vote_average": details.get("vote_average", 0),
            "vote_count": details.get("vote_count", 0),
            "reddit_volume": reddit_volume,
            "sentiment_score": reddit_sentiment,
            "avg_upvotes": reddit_upvotes,
            "tmdb_sentiment_score": tmdb_sentiment,
            "tmdb_avg_rating": tmdb_rating,
            "tmdb_review_count": tmdb_count,
        }

        # Add encoded categories (genre, language, production company)
        if details.get("genres"):
            genre_name = details["genres"][0]['name']
            data_film[f"genre_{genre_name}"] = 1
        lang = details.get("original_language", "")
        data_film[f"original_language_{lang}"] = 1
        if details.get("production_companies"):
            prod_name = details["production_companies"][0]['name']
            data_film[f"production_companies_{prod_name}"] = 1

        #  Format input like the training dataset
        df_ref = pd.read_csv("data/films_ready.csv")
        colonnes_ref = df_ref.drop(columns=["success"]).columns
        df_input = pd.DataFrame([data_film])
        for col in colonnes_ref:
            if col not in df_input.columns:
                df_input[col] = 0
        df_input = df_input[colonnes_ref]

        #  Load the model and predict
        model = joblib.load("models/random_forest.pkl")
        pred = model.predict(df_input)[0]
        proba = model.predict_proba(df_input)[0][1]

        print("\n Prediction result:")
        if pred == 1:
            print(f" Likely success (confidence: {round(proba * 100)}%)")
        else:
            print(f" Likely failure (confidence: {round((1 - proba) * 100)}%)")
    else:
        print(" Movie not found.")
