from flask import jsonify
from vector_clocks import VectorClock

NODE_ID = "A"  # later this could be set via env variable

kv_store = {}
vc = VectorClock(NODE_ID)


def store(key, value, metadata):
    stored = kv_store.get(key)

    if stored:
        _, stored_clock = stored
        if vc.is_concurrent_with(client_clock, stored_clock):
            # Conflict: both client and store made different changes
            return jsonify({
                "error": "Conflict detected",
                "message": "Concurrent updates",
                "causal-metadata": stored_clock
            }), 409

        elif is_older(client_clock, stored_clock):
            # Client is behind — reject or return latest
            return jsonify({
                "message": "Client metadata is outdated",
                "causal-metadata": stored_clock
            }), 200

    # Accept and apply the write
    vc.update(client_clock)
    vc.increment()
    current_clock = vc.get()
    kv_store[key] = (value, current_clock)

    return jsonify({"message": "Stored", "causal-metadata": current_clock}), 200

    # vc.increment()  # log a new event by this node
    # current_clock = vc.get()  # get the updated clock state
    # kv_store[key] = (value, current_clock)

    # return jsonify({"message": "Stored", "causal-metadata": current_clock}), 200


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

def is_older(client_clock, stored_clock):
    for node in set(stored_clock) | set(client_clock):
        if client_clock.get(node, 0) > stored_clock.get(node, 0):
            return False
    return client_clock != stored_clock

def is_same(clock1, clock2):
    return clock1 == clock2


# Add this method to your VectorClock class (or define as external function)
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
