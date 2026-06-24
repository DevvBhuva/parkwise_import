import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# ---------- CONFIG ----------
SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"
CSV_PATH = "cities_and_sub_areas.csv"
COLLECTION_NAME = "locations"
# ----------------------------

# Initialize Firebase Admin
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Read CSV
df = pd.read_csv(CSV_PATH)

for _, row in df.iterrows():
    city_id = row["city_id"]
    city_name = row["city_name"]
    area_id = row["area_id"]
    area_name = row["area_name"]

    # Create / Update city document
    city_ref = db.collection(COLLECTION_NAME).document(city_id)
    city_ref.set(
        {"name": city_name},
        merge=True
    )

    # Create area sub-collection
    area_ref = city_ref.collection("areas").document(area_id)
    area_ref.set({
        "name": area_name
    })

print("✅ Locations collection created successfully.")
