from pathlib import Path

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "sensors_reading.csv"
MODEL_PATH = PROJECT_ROOT / "ml" / "plant_model.pkl"


# --------------------------------------------------
# Load dataset and trained model
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

saved_data = joblib.load(MODEL_PATH)

model = saved_data["model"]
features = saved_data["features"]


# --------------------------------------------------
# Prepare data
# --------------------------------------------------

X = df[features]
y = df["label"]


# --------------------------------------------------
# Create separate test dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# Evaluate on unseen test data
# --------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Evaluation Results")
print("------------------------")
print(f"Test Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))