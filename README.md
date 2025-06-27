# SyncKV: A Distributed Causally Consistent Key-Value Store

SyncKV is a distributed key-value store designed to support **causal consistency** using **vector clocks** and periodic **gossip-based synchronization** between nodes. The system is implemented in Python using Flask and containerized with Docker.

This project emulates the core principles found in distributed systems like Amazon DynamoDB and Riak. It emphasizes fault tolerance, eventual consistency, and decentralized design.

---

## Author

**Manikanta Illuri**  
B.S. Computer Science  
University of California, Santa Cruz

---

## Features

- Causal consistency using vector clocks
- Conflict detection based on concurrent updates
- Gossip protocol to propagate updates every 3 seconds
- Dynamic cluster view configuration through admin APIs
- RESTful HTTP interface using Flask
- Docker-based deployment for cross-platform compatibility

---

## API Endpoints

### `/kvs/data/<key>`

| Method   | Description                                          |
| -------- | ---------------------------------------------------- |
| `PUT`    | Stores a key with a value and causal metadata        |
| `GET`    | Retrieves the key’s value if the client is not ahead |
| `DELETE` | Deletes the key if the client clock is not behind    |

### `/kvs/admin/view`

| Method | Description                              |
| ------ | ---------------------------------------- |
| `PUT`  | Updates the list of nodes in the cluster |
| `GET`  | Retrieves the current node view          |

### `/kvs/internal/sync`

| Method | Description                                          |
| ------ | ---------------------------------------------------- |
| `POST` | Accepts gossip-based synchronization data from peers |

---

## Running the System Locally

### Step 1: Build the Docker image

```bash
docker build -t synckv .
```

### Step 2: Start a node

```bash
docker run -p 8001:8080 -e NODE_ID=A synckv
```

This runs Node A on `localhost:8001`.

### Step 3: Configure the view

In a new terminal:

```bash
curl -X PUT -H "Content-Type: application/json" \
-d '{"view": ["localhost:8001"]}' \
http://localhost:8001/kvs/admin/view
```

### Step 4: Store and retrieve a key

```bash
curl -X PUT -H "Content-Type: application/json" \
-d '{"val": "hello", "causal-metadata": {}}' \
http://localhost:8001/kvs/data/greeting

curl -X GET -H "Content-Type: application/json" \
-d '{"causal-metadata": {}}' \
http://localhost:8001/kvs/data/greeting
```

---

## How It Works

Each node maintains a vector clock to track the causal history of updates. Clients send causal metadata along with each request. The server uses this metadata to determine whether to accept, reject, or delay an operation, ensuring updates respect causal order.

Every node runs a background gossip thread that periodically sends its current data and vector clocks to other nodes in the view. This allows nodes to stay in sync without a central coordinator. If a node goes offline, it will catch up once it rejoins and receives gossip updates.

---

## Development Environment

- Python 3.9
- Flask
- Docker
- curl (for API testing)

---
