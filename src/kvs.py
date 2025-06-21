from flask import jsonify
from vector_clocks import VectorClock

NODE_ID = "A"
vc = VectorClock(NODE_ID)
kv_store = {}

def store(key, value, metadata):
    stored = kv_store.get(key)

    if stored:
        _, stored_clock = stored
        if is_concurrent_with(vc, metadata, stored_clock):
            return jsonify({
                "error": "Conflict detected",
                "message": "Concurrent updates",
                "causal-metadata": stored_clock
            }), 409
        elif is_older(metadata, stored_clock):
            return jsonify({
                "message": "Client metadata is outdated",
                "causal-metadata": stored_clock
            }), 200

    vc.update(metadata)
    vc.increment()
    current_clock = vc.get()
    kv_store[key] = (value, current_clock)

    return jsonify({"message": "Stored", "causal-metadata": current_clock}), 200

def retrieve(key, metadata):
    if key not in kv_store:
        return jsonify({"error": "Key not found"}), 404

    value, stored_clock = kv_store[key]

    if is_older(metadata, stored_clock):
        return jsonify({"val": value, "causal-metadata": stored_clock}), 200
    else:
        return jsonify({"message": "No new update", "causal-metadata": stored_clock}), 200

def delete(key, metadata):
    if key not in kv_store:
        return jsonify({"error": "Key not found"}), 404

    _, stored_clock = kv_store[key]

    if is_older(metadata, stored_clock):
        return jsonify({
            "message": "Delete rejected: client clock is behind",
            "causal-metadata": stored_clock
        }), 200

    vc.update(metadata)
    vc.increment()
    del kv_store[key]
    return jsonify({
        "message": "Deleted",
        "causal-metadata": vc.get()
    }), 200

def is_older(client_clock, stored_clock):
    for node in set(stored_clock) | set(client_clock):
        if client_clock.get(node, 0) > stored_clock.get(node, 0):
            return False
    return client_clock != stored_clock

def is_same(clock1, clock2):
    return clock1 == clock2

def is_concurrent_with(vc, c1, c2):
    greater = lesser = False
    for node in set(c1) | set(c2):
        a = c1.get(node, 0)
        b = c2.get(node, 0)
        if a < b:
            lesser = True
        elif a > b:
            greater = True
    return greater and lesser
