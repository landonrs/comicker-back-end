#!/bin/bash
aws dynamodb create-table --cli-input-json file://dynamo-local/comic-table.json --endpoint-url http://localhost:8000