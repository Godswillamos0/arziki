"""
Inference script for supermarket sales prediction.
Loads a trained RandomForest model and encoders,
then predicts QuantitySold for a new store inventory CSV.
"""

import pandas as pd
import joblib
import os


# ==============================
# CONFIGURATION
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "sales_predictor.pkl")


ENCODER_PATH = os.path.join(BASE_DIR, "encoders.pkl")
#csv_file = os.path.join(BASE_DIR, "new_inventory.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "predicted_sales.csv")

def run_inference(csv_file):
    # ==============================
    # LOAD MODEL AND ENCODERS
    # ==============================
    print("🔄 Loading model and encoders...")
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODER_PATH)
    print("✅ Model and encoders loaded successfully.\n")

    # ==============================
    # LOAD NEW INVENTORY DATA
    # ==============================
    print(f"📦 Reading input file: {csv_file}")
    try:
        new_df = pd.read_csv(csv_file, encoding="latin1")
    except FileNotFoundError:
        raise SystemExit(f"❌ File '{csv_file}' not found. Make sure it's in the same folder.")

    print(f"✅ Loaded {len(new_df)} records.\n")

    # ==============================
    # PREPROCESSING
    # ==============================
    required_columns = ['City', 'Area', 'ProductName', 'QuantityAvailable', 'Cost', 'RetailPrice']
    missing_cols = [c for c in required_columns if c not in new_df.columns]

    if missing_cols:
        raise ValueError(f"❌ Missing columns in input CSV: {missing_cols}")

    # Keep a copy of the original (for readable output)
    encoded_df = new_df.copy()

    # Encode categorical columns safely (handle unseen labels)
    for col in ['City', 'Area', 'ProductName']:
        encoder = encoders[col]
        encoded_df[col] = encoded_df[col].apply(
            lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1
        )

    # Prepare features
    X_new = encoded_df[['City', 'Area', 'ProductName', 'QuantityAvailable', 'Cost', 'RetailPrice']]

    # ==============================
    # PREDICTION
    # ==============================
    print("🔮 Making predictions...")
    predictions = model.predict(X_new)
    new_df['Predicted_QuantitySold'] = predictions

    # ==============================
    print("\n📊 Preview of results:")
    print(new_df[['City', 'Area', 'ProductName', 'Predicted_QuantitySold']].head())
    return new_df[['City', 'Area', 'ProductName', 'Predicted_QuantitySold']].head()
