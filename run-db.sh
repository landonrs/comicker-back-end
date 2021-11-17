#!/bin/bash
cd postgres-local
docker-compose up -d --remove-orphans
psql -h localhost -p 5432 -U docker -d comicker
cd ..