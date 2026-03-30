# Box Office Predictor

Predicting Movie Box Office Success using TMDB + Reddit + Machine Learning

This project predicts the box office success of movies by combining TMDB metadata, Reddit social signals, and a Random Forest machine learning model.

## Installation
### Prerequisites
Python 3.11 or higher.  
Conda (for environment management) or pip.  
TMDB API key: You can get a TMDB API key by signing up on TMDB.  
Reddit API key: For fetching Reddit data (see fetch_reddit_posts.py).

### **Installation Steps**

### Clone this repository:**

git clone https://github.com/monalisasdi/boxoffice-predictor.git  
cd boxoffice-predictor

### Create a Conda environment (recommended):**

conda create -n boxoffice-env python=3.11  
conda activate boxoffice-env

### Install the dependencies:**

pip install -r requirements.txt

### Install dotenv (if needed for environment variable management):**

pip install python-dotenv

### Preparing the Data**
1. Download the movie dataset from Kaggle

Download the TMDB Movies Dataset 2023 (930,000 movies) from this Kaggle link : https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies

Once downloaded, unzip the file and place it in the data/ folder as films.csv.

2. Run the script to filter movies

This script generates a sample of 50,000 movies from the films.csv file for easier processing.

python filtrer.py

This will create the films_50000.csv file in the data/ folder.

3. Fetch Reddit data 

The project enriches the movies with data from Reddit. Run the fetch_reddit_posts.py script to fetch Reddit posts associated with the movies. Make sure you have set up your Reddit API keys in the environment variables (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT).

python fetch_reddit_posts.py

This will generate the films_with_reddit.csv file containing additional information such as the volume of Reddit discussions, sentiment scores, and upvotes.

4. Merge datasets

After enriching the movies with Reddit data, you can merge them with the base movie data. Run the merge_datasets.py script:

python merge_datasets.py

This will create the films_merged.csv file, combining information from films_50000.csv and films_with_reddit.csv.

5. Fetch TMDB reviews

This script enriches the merged movies with TMDB reviews. Run fetch_tmdb_reviews.py to fetch reviews for the movies and enrich the data with sentiment scores, average ratings, and the number of reviews.

Make sure you have set up your TMDB API key in the environment variables (TMDB_API_KEY).

python fetch_tmdb_reviews.py

This will generate films_with_tmdb.csv with the TMDB reviews.

6. Prepare the final dataset

Once all data has been merged and enriched, run prepare_dataset.py to clean and prepare the data for analysis.

python prepare_dataset.py

This will create the films_ready.csv file, ready for analysis and prediction.

### Training the Model

Once the data is prepared, you can train the Random Forest model to predict movie box office success.

python train_model.py

This will train the model and save the results in a model file (e.g., random_forest.pkl).

### Automatic Box Office Prediction

Once the model is trained, you can predict the box office success of a movie automatically using its title. Run predict_auto.py to enter a movie title and get a prediction.

python predict_auto.py

Example input:

Enter movie title: Avengers: Endgame

Expected output:

Movie Title: Avengers: Endgame
Predicted Success Score: 0.85
Confidence Estimate: 0.90
Project Structure

## The project is structured as follows:

BoxOfficePredictor/  
├── analysis/   
│   ├── prepare_dataset.py  # Prepares the dataset  
│   ├── train_model.py      # Trains the model  
├── data/  
│   ├── films.csv           # Base movie dataset (to be downloaded from Kaggle)  
│   ├── films_50000.csv     # Sample of the first 50,000 movies  
│   ├── films_with_reddit.csv  # Movies enriched with Reddit data  
│   ├── films_merged.csv    # Merged data from films and Reddit  
│   ├── films_with_tmdb.csv # Movies enriched with TMDB reviews  
│   └── films_ready.csv     # Cleaned and prepared data for analysis  
├── models/  
│   ├── random_forest.pkl   # Random Forest model file  
├── reddit/  
│   ├── fetch_reddit_posts.py # Fetches Reddit posts for each movie  
│   ├── reddit_test.py         # Test Reddit functions  
├── .env                     # Environment variables (API keys)  
├── .gitignore               # Files to be ignored by Git  
├── predict_auto.py          # Auto-prediction for a movie title  
├── filtrer.py               # Filters and creates the movie sample  
├── merge_datasets.py        # Merges the datasets  
├── requirements.txt         # List of Python dependencies  
└── README.md                # Project documentation  

## Conclusion

This project explores how Reddit social signals and TMDB metadata can be used to predict a movie's commercial success. It offers valuable insights for studios, marketing teams, distributors, and entertainment analysts.

