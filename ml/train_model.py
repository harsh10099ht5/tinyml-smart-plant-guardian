from pathlib import Path

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "sensors_reading.csv"
MODEL_PATH = PROJECT_ROOT / "ml" / "plant_model.pkl"


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully.")
print(f"Dataset shape: {df.shape}")
print("\nAvailable columns:")
print(df.columns.tolist())


# --------------------------------------------------
# 3. Define features and target
# --------------------------------------------------

features = [
    "soil_moisture",
    "temperature",
    "humidity",
    "hours_since_watering"
]

target = "label"


# --------------------------------------------------
# 4. Validate required columns
# --------------------------------------------------

required_columns = features + [target]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns in dataset: {missing_columns}"
    )


# --------------------------------------------------
# 5. Prepare input and output data
# --------------------------------------------------

X = df[features]
y = df[target]

print("\nClass distribution:")
print(y.value_counts())


# --------------------------------------------------
# 6. Split dataset into training and testing data
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# 7. Create Random Forest model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=6,
    random_state=42,
    class_weight="balanced"
)


# --------------------------------------------------
# 8. Train the model
# --------------------------------------------------

print("\nTraining model...")

model.fit(X_train, y_train)

print("Model training completed.")


# --------------------------------------------------
# 9. Evaluate the model
# --------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:")
print(f"{accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# --------------------------------------------------
# 10. Save trained model
# --------------------------------------------------

joblib.dump(
    {
        "model": model,
        "features": features
    },
    MODEL_PATH
)

print("\nModel saved successfully.")
print(f"Saved at: {MODEL_PATH}")