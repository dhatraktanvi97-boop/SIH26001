import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# ---------------------------------------
# DEMO TRAINING DATA
# ---------------------------------------
# Temporary training data for our prototype.
# We will replace this with real USGS data.

np.random.seed(42)

data = pd.DataFrame({
    "rainfall": np.random.uniform(0, 300, 1000),
    "soil_moisture": np.random.uniform(0, 100, 1000),
    "ground_movement": np.random.uniform(0, 20, 1000),
    "water_level": np.random.uniform(0, 100, 1000)
})

# Create temporary training labels
risk_score = (
    data["rainfall"] * 0.35 +
    data["soil_moisture"] * 0.25 +
    data["ground_movement"] * 2.5 +
    data["water_level"] * 0.15
)

data["risk"] = pd.cut(
    risk_score,
    bins=[-1, 40, 70, 1000],
    labels=["LOW", "MEDIUM", "HIGH"]
)

# ---------------------------------------
# FEATURES AND TARGET
# ---------------------------------------

X = data[
    [
        "rainfall",
        "soil_moisture",
        "ground_movement",
        "water_level"
    ]
]

y = data["risk"]

# ---------------------------------------
# TRAIN / TEST SPLIT
# ---------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------------------------------------
# MACHINE LEARNING MODEL
# ---------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------------------------------
# TEST MODEL
# ---------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model trained successfully!")
print(f"Accuracy: {accuracy * 100:.2f}%")

# ---------------------------------------
# SAVE MODEL
# ---------------------------------------

joblib.dump(
    model,
    "ai_model/landslide_model.pkl"
)

print("Model saved as:")
print("ai_model/landslide_model.pkl")
     