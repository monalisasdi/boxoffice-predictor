# Box Office Predictor
Predicting Movie Box Office Success using TMDB + Reddit + Machine Learning

## 1. Create a new Python 3.11 environment
conda create -n boxoffice-env python=3.11

## 2. Activate the environment
conda activate boxoffice-env

## 3. Install required libraries
pip install pandas snscrape

## Box Office Predictor  
Predicting Movie Box Office Success using TMDB + Reddit + Machine Learning

This project predicts a movie’s box office success by combining TMDB metadata, Reddit social signals, and a Random Forest machine learning model.

It automates:
- Movie data collection (TMDB)
- Reddit posts & engagement extraction
- Dataset merging & preprocessing
- Model training
- Automated prediction for any movie title

### Features

- TMDB movie metadata
- Reddit hype & engagement signals
- Sentiment analysis
- Feature engineering
- Random Forest model training
- Automated prediction pipeline

---


---

## Installation

### 1. Create environment (recommended)

conda create -n boxoffice-env python=3.11
conda activate boxoffice-env

### 2. Install dependencies
pip install -r requirements.txt

### Install dotenv if needed:

pip install python-dotenv

### Prepare Dataset
python analysis/prepare_dataset.py

### Train the Model
python analysis/train_model.py

### Predict Movie Box Office Automatically
python predict_auto.py

You can enter:
Movie title

Output:
Predicted success score
Confidence estimate

### Model
Algorithm: Random Forest
Input: Movie + Reddit features
Output: Box office success prediction

### Project Objective : 
This project explores how online hype, audience sentiment, and movie metadata can help predict commercial movie success, offering insights for:
Studios
Marketing teams
Distributors
Entertainment analysts

Author : Saadi Mouna Lisa
Data Analytics & Machine Learning

