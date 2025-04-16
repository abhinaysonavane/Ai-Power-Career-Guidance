import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import pickle

# Load data
df = pd.read_excel("data/Career Rec System_updated.xlsx", engine='openpyxl')

# Clean and prepare data
df = df.dropna(subset=["Skills", "Recommended Career"])
X = df["Skills"]
y = df["Recommended Career"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline: TF-IDF + Logistic Regression
model = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))
model.fit(X_train, y_train)

# Save model
with open("model/career_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to model/career_model.pkl")
