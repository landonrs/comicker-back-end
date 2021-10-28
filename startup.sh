#!/bin/bash
sam build --use-container
sam local start-api --docker-network local-dynamodb \
--skip-pull-image --profile comicker-local \
--parameter-overrides 'ParameterKey=StageName,ParameterValue=local' \
-p 8080
