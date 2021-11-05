#!/bin/bash
export AWS_SDK_LOAD_CONFIG=true
sam build --use-container
sam local start-api --docker-network local-dynamodb \
--skip-pull-image --profile comicker-lambda-role \
--parameter-overrides 'ParameterKey=System,ParameterValue=local' \
-p 8080
