
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, storage

# Load the JSON string from Render environment variable
cred_data = json.loads(os.getenv("FIREBASE_CREDENTIALS_JSON"))

# Initialize Firebase app with both Firestore and Cloud Storage
cred = credentials.Certificate(cred_data)
firebase_admin.initialize_app(cred, {
    "storageBucket": f"{cred_data['project_id']}.appspot.com"
})

# Clients to be used across app
db = firestore.client()
bucket = storage.bucket()

# Save feature metadata to Firestore under /projects/{project}
def save_feature_to_firestore(project, feature_data):
    doc_ref = db.collection("projects").document(project)
    doc_ref.set({"features": firestore.ArrayUnion([feature_data])}, merge=True)

# Upload code (as string) to Cloud Storage as a file
def upload_agent_file(project, filename, content):
    blob = bucket.blob(f"{project}/{filename}")
    blob.upload_from_string(content)
    return blob.public_url
