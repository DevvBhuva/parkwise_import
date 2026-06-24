import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import math

# ---------- Firebase Init ----------
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------- Helper ----------
def safe_int(value):
    if pd.isna(value):
        return 0
    return int(value)

# ---------- Read CSV ----------
df = pd.read_csv("parking_details.csv")

# ---------- Upload ----------
for _, row in df.iterrows():
    parking_id = str(row["parking_id"]).strip()

    supported_list = [
        v.strip() for v in str(row["supported_vehicles"]).split(",") if v.strip()
    ]

    db.collection("parkings").document(parking_id).set({
        "parking_name": row["parking_name"],
        "landmark": row["landmark"],
        "timings": row["timings"],

        "location": {
            "longitude": float(row["longitude"]),
            "latitude": float(row["latitude"])
        },

        "facility": row["facility"],
        "supported_vehicles": supported_list,

        "prices": {
            "bike": safe_int(row["price_bike"]),
            "hatchback": safe_int(row["price_hatchback"]),
            "sedan": safe_int(row["price_sedan"]),
            "suv": safe_int(row["price_suv"]),
            "ev": safe_int(row["price_ev"])
        },

        "slots": {
            "bike": safe_int(row["slots_bike"]),
            "hatchback": safe_int(row["slots_hatchback"]),
            "sedan": safe_int(row["slots_sedan"]),
            "suv": safe_int(row["slots_suv"]),
            "ev": safe_int(row["slots_ev"])
        }
    })

print("✅ CSV imported successfully into Firestore")
