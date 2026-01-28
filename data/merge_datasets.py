import pandas as pd

# Load both files
films_base = pd.read_csv("data/films_50000.csv")
films_reddit = pd.read_csv("data/films_with_reddit.csv")

# Merge on title (watch out for duplicates or extra spaces)
merged = pd.merge(films_base, films_reddit, on="title", how="inner")

# Save merged result
merged.to_csv("data/films_merged.csv", index=False)

print("✅ Merge completed: data/films_merged.csv")
print(f"Merged movies: {len(merged)}")
