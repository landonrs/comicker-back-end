#!/bin/bash
sam local start-api --docker-network local-dynamodb \
--skip-pull-image --profile default \
--parameter-overrides 'ParameterKey=StageName,ParameterValue=local' \
-p 8080
