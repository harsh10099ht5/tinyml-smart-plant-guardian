import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("../data/sensor_readings.csv")

features = [
    "soil_moisture",
    "temperature",
    "humidity",
    "hours_since_watering"
]

X = df[features]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=50,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

joblib.dump(model, "plant_model.pkl")