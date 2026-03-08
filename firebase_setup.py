import firebase_admin
from firebase_admin import credentials, firestore
import config

# Initialize Firebase
cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_firestore_client():
    return db