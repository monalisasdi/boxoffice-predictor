import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

# Load enriched dataset
df = pd.read_csv("data/films_with_tmdb.csv")

print(f"🎬 Movies loaded: {len(df)}")

# Numeric columns to convert
cols_num = [
    'budget', 'revenue', 'popularity', 'runtime',
    'vote_average', 'vote_count',
    'reddit_volume', 'sentiment_score', 'avg_upvotes',
    'tmdb_sentiment_score', 'tmdb_avg_rating'
]

for col in cols_num:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove movies without budget or revenue
df = df.dropna(subset=['budget', 'revenue'])
df = df[(df['budget'] > 0) & (df['revenue'] > 0)]

# Target variable: success = 1 if revenue > 1.3 × budget
df['success'] = (df['revenue'] > 1.3 * df['budget']).astype(int)

# Indicators for social data availability
df['has_reddit'] = (df['reddit_volume'] > 0).astype(int)
df['has_tmdb'] = (df['tmdb_review_count'] > 0).astype(int)

# Multi-hot encoding for genres
df['genres'] = df['genres'].astype(str).apply(lambda x: x.split('-'))
mlb = MultiLabelBinarizer()
genres_encoded = pd.DataFrame(
    mlb.fit_transform(df['genres']),
    columns=[f"genre_{g}" for g in mlb.classes_]
)
df = pd.concat([df, genres_encoded], axis=1)
df.drop(columns=['genres'], inplace=True)

# Simplify production_companies: keep only the first one
df['production_companies'] = df['production_companies'].astype(str).apply(
    lambda x: x.split('-')[0].strip()
)

# Keep only the top 20 most frequent companies + "Other"
top_companies = df['production_companies'].value_counts().nlargest(20).index
df['production_companies'] = df['production_companies'].apply(
    lambda x: x if x in top_companies else 'Other'
)

# Encode original_language and production_companies
df = pd.get_dummies(
    df,
    columns=['original_language', 'production_companies'],
    drop_first=True
)

# Columns to drop (not useful for modeling)
drop_cols = [
    'poster_path', 'backdrop_path', 'overview', 'tagline',
    'credits', 'keywords', 'recommendations', 'reddit_texts',
    'status', 'release_date', 'title', 'id'
]

df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)

# Export final dataset
df.to_csv("data/films_ready.csv", index=False)
print(f" Dataset ready: {len(df)} movies → data/films_ready.csv")
