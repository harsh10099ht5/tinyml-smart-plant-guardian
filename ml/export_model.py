from pathlib import Path
import json
import joblib


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "ml" / "plant_model.pkl"
OUTPUT_PATH = PROJECT_ROOT / "ml" / "model_metadata.json"


# --------------------------------------------------
# Check model file
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        "plant_model.pkl not found. Run train_model.py first."
    )


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

saved_data = joblib.load(MODEL_PATH)

model = saved_data["model"]
features = saved_data["features"]


# --------------------------------------------------
# Prepare model metadata
# --------------------------------------------------

metadata = {
    "model_type": "RandomForestClassifier",
    "features": features,
    "classes": model.classes_.tolist(),
    "number_of_trees": model.n_estimators,
    "maximum_depth": model.max_depth,
    "random_state": model.random_state,
    "deployment_target": "ESP32",
    "status": "Prototype model for educational use"
}


# --------------------------------------------------
# Save metadata as JSON
# --------------------------------------------------

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        metadata,
        file,
        indent=4
    )


print("Model metadata exported successfully.")
print(f"Saved at: {OUTPUT_PATH}")