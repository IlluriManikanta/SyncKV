from flask import Flask, request, jsonify
from kvs import store, retrieve, delete
from admin import put_view, get_view
from sync import gossip
from internal import sync_data
import threading

app = Flask(__name__)

@app.route("/kvs/data/<key>", methods=["PUT"])
def put_key(key):
    data = request.get_json()
    value = data.get("val")
    metadata = data.get("causal-metadata", {})
    return store(key, value, metadata)

@app.route("/kvs/data/<key>", methods=["GET"])
def get_key(key):
    metadata = request.get_json().get("causal-metadata", {})
    return retrieve(key, metadata)

@app.route("/kvs/data/<key>", methods=["DELETE"])
def delete_key(key):
    metadata = request.get_json().get("causal-metadata", {})
    return delete(key, metadata)

@app.route("/kvs/admin/view", methods=["PUT"])
def update_view():
    return put_view()

@app.route("/kvs/admin/view", methods=["GET"])
def fetch_view():
    return get_view()

@app.route("/kvs/internal/sync", methods=["POST"])
def internal_sync():
    return sync_data()

threading.Thread(target=gossip, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)