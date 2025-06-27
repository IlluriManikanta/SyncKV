import threading
import time
import requests
from globals import view
from kvs import kv_store, vc

def gossip():
    while True:
        time.sleep(3)
        for node in view:
            try:
                data = {
                    "store": kv_store,
                    "vector_clock": vc.get()
                }
                requests.post(f"http://{node}/kvs/internal/sync", json=data, timeout=1)
            except:
                pass  # node may be down, that's okay