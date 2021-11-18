#!/bin/bash
cd postgres-local
docker-compose up -d
#psql -h localhost -p 5432 -U docker -d comicker
cd ..