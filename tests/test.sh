#!/bin/bash

curl -X PUT -d '{"view":["10.10.0.3:8000"]}' -H 'Content-Type: application/json' http://localhost:8000/kvs/admin/view -w '\nStatus: %{http_code}\n\n'

curl -X GET -d '{}' -H 'Content-Type: application/json' http://localhost:8000/kvs/admin/view -w '\nStatus: %{http_code}\n\n'

curl -X PUT -d '{"val": "sampleVal", "causal-metadata": {}}' -H 'Content-Type: application/json' http://localhost:8000/kvs/data/x -w '\nStatus: %{http_code}\n\n'

curl -X GET -d '{"causal-metadata": {"x": [1]}}' -H 'Content-Type: application/json' http://localhost:8000/kvs/data/x -w '\nStatus: %{http_code}\n\n'

curl -X PUT -d '{"val": "hello", "causal-metadata": {}}' -H 'Content-Type: application/json' http://localhost:8000/kvs/data/y -w '\nStatus: %{http_code}\n\n'

curl -X GET -d '{"causal-metadata": {"x": [1]}}' -H 'Content-Type: application/json' http://localhost:8000/kvs/data/y -w '\nStatus: %{http_code}\n\n'

curl -X PUT -d '{"val": "hello2", "causal-metadata": {"x": [1], "y": [1]}}' -H 'Content-Type: application/json' http://localhost:8000/kvs/data/y -w '\nStatus: %{http_code}\n\n'

curl -X GET -d '{"causal-metadata": {"x": [1]}}' -H 'Content-Type: application/json' http://localhost:8000/kvs/data/y -w '\nStatus: %{http_code}\n\n'

curl -X DELETE -d '{"causal-metadata": {"x": [1]}}' -H 'Content-Type: application/json' http://localhost:8000/kvs/data/y -w '\nStatus: %{http_code}\n\n'

curl -X GET -d '{"causal-metadata": {"x": [1]}}' -H 'Content-Type: application/json' http://localhost:8000/kvs/data/y -w '\nStatus: %{http_code}\n\n'
