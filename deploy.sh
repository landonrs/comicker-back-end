sam package --output-template-file packaged.yaml --s3-bucket comicker-api-lambda-source-bucket --profile comicker-deployment --region us-east-1
# sam deploy --profile comicker-deployment --region us-east-1 --stack-name comicker-api
sam deploy --template-file ./packaged.yaml --profile comicker-deployment --stack-name comicker-api
