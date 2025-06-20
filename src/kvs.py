from flask import jsonify

kv_store = {}

def store(key, value, metadata):
    kv_store[key] = value
    return jsonify({"message": "Stored", "causal-metadata": {}}), 200

def retrieve(key, metadata):
    if key in kv_store:
        return jsonify({"val": kv_store[key], "causal-metadata": {}}), 200
    return jsonify({"error": "Key not found"}), 404

def delete(key, metadata):
    if key in kv_store:
        del kv_store[key]
        return jsonify({"message": "Deleted", "causal-metadata": {}}), 200
    return jsonify({"error": "Key not found"}), 404
