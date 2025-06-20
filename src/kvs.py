from flask import jsonify
from vector_clocks import VectorClock

NODE_ID = "A"  # later this could be set via env variable

kv_store = {}
vc = VectorClock(NODE_ID)


def store(key, value, metadata):
    vc.increment()  # log a new event by this node
    current_clock = vc.get()  # get the updated clock state
    kv_store[key] = (value, current_clock)

    return jsonify({"message": "Stored", "causal-metadata": current_clock}), 200


def retrieve(key, metadata):
    if key in kv_store:
        value, stored_clock = kv_store[key]
        return jsonify({"val": value, "causal-metadata": stored_clock}), 200

    return jsonify({"error": "Key not found"}), 404

def delete(key, metadata):
    if key in kv_store:
        vc.increment()
        del kv_store[key]
        return jsonify({"message": "Deleted", "causal-metadata": vc.get()}), 200

    return jsonify({"error": "Key not found"}), 404
