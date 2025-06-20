from flask import Flask, request, jsonify
from kvs import store, retrieve, delete

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
