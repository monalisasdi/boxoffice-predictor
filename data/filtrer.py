import pandas as pd

# Load the original dataset
df = pd.read_csv("data/films.csv")

# Keep the first 50,000 movies
df_sample = df.head(50000)

# Save to a new file
df_sample.to_csv("data/films_50000.csv", index=False)
print("✅ Sample of 50,000 movies created: data/films_50000.csv")
