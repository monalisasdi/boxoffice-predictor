import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import joblib

# Load prepared dataset
df = pd.read_csv("data/films_ready.csv")

# Remove rows without defined success label
df = df.dropna(subset=['success'])

# Define X (features) and y (target)
X = df.drop(columns=['success'])
y = df['success']

# Split into train / test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("Classification report:")
print(classification_report(y_test, y_pred))

print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))

# Feature importance
importances = model.feature_importances_
features = X.columns
importances_df = pd.DataFrame({'feature': features, 'importance': importances})
importances_df = importances_df.sort_values(by='importance', ascending=False)

# Plot
plt.figure(figsize=(10, 6))
plt.barh(importances_df['feature'][:20][::-1], importances_df['importance'][:20][::-1])
plt.xlabel('Importance')
plt.title('Top 20 most important features')
plt.tight_layout()
plt.show()

# Save model
joblib.dump(model, "models/random_forest.pkl")
print("Model saved to models/random_forest.pkl")
