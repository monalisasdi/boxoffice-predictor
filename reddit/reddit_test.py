import praw

# Reddit authentication
reddit = praw.Reddit(
    client_id="MOR2kDcCeFvf0ZGC1-i8Yg",
    client_secret="4tr3seufYxScsdkN4qN8S9nUfINV5g",
    user_agent="boxoffice script by u/Effective_Science_41"
)

# Search for posts related to a movie
query = "Dune Part Two"
subreddit = reddit.subreddit("movies")

print(f"🔍 Results for: {query}")
for post in subreddit.search(query, limit=10):
    print("----")
    print("Title:", post.title)
    print("Score:", post.score)
    print("Date:", post.created_utc)
    print("Text:", post.selftext[:200])
