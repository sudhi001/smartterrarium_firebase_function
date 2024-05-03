
# The Firebase Admin SDK to access Cloud Firestore.
from typing import Any
from firebase_admin import initialize_app, db,firestore
from firebase_functions import db_fn
from datetime import datetime

# Initialize Firebase app
app = initialize_app()


# Define the function to listen for value creation events
@db_fn.on_value_created(reference="/sensors/{deviceId}",region="asia-southeast1")
def listen_sensor_data_on_creation(event: db_fn.Event[Any]) -> None:
    original = event.data
    deviceId = event.params['deviceId']
    firestore_client = firestore.Client()
    original["timestamp"] = datetime.now().isoformat()
    # Define the collection reference
    collection_ref = firestore_client.collection('device_logs')
    # Generate a unique document ID
    doc_id = f"{deviceId}_{datetime.now().isoformat()}"
    # Set the data in Firestore
    doc_ref = collection_ref.document(doc_id)
    doc_ref.set(original)

@db_fn.on_value_updated(reference="/sensors/{deviceId}",region="asia-southeast1")
def listen_sensor_data_updated(event: db_fn.Event[Any]) -> None:
    change = event.data
    deviceId = event.params['deviceId']
    firestore_client = firestore.Client()
    # Get the new data
    new_data = change.after if change.after else {}

    new_data["timestamp"] = datetime.now().isoformat()
    # Define the collection reference
    collection_ref = firestore_client.collection('device_logs')
    # Generate a unique document ID
    doc_id = f"{deviceId}_{datetime.now().isoformat()}"
    # Set the data in Firestore
    doc_ref = collection_ref.document(doc_id)
    doc_ref.set(new_data)