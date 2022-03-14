import firebase_admin
from firebase_admin import credentials, firestore, storage

## privateKey must be from your Firebase project
cred = credentials.Certificate("./serviceAccountKey.json")

## Firestore and Cloud Storage access
db = firestore.client()
bucket = storage.bucket()
