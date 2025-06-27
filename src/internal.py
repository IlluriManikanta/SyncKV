from flask import request, jsonify
from kvs import store

def sync_data():
    data = request.get_json()
    incoming_store = data.get("store", {})

    for key, (val, metadata) in incoming_store.items():
        store(key, val, metadata)

    return jsonify({"message": "Sync successful"}), 200