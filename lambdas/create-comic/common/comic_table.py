import decimal
from typing import Dict

import boto3
from botocore.exceptions import ClientError
from datetime import datetime


"""
REALLY JANKY, but REMEMBER TO COPY THIS INTO EVERY LAMBDA DIRECTORY WHEN DONE DEVELOPING!!!
"""

TABLE_NAME = "comicTable"
LOCAL_ENDPOINT = "http://dynamo:8000"
LAST_EVALUATED_KEY = "LastEvaluatedKey"
PAGE_LIMIT = 5



class ComicTable:
    def __init__(self):
        self.table = boto3.session.Session().resource('dynamodb', endpoint_url=LOCAL_ENDPOINT).Table(
            TABLE_NAME)

    def get_comic(self, comic_id):
        try:
            response = self.table.get_item(
                Key={
                    "comicId": comic_id
                }
            )
            return response.get('Item', {})
        except ClientError as e:
            print(f"Exception occurred {e}")

    def put_comic(self, comic_data):
        try:
            response = self.table.put_item(
                Item=comic_data
            )
            return response
        except ClientError as e:
            print(f"Exception occurred {e}")
            raise e

    def get_comics(self):
        cleaned_comics = []
        print("getting comics")
        try:
            response = self.table.scan(
            )
            comics = response.get("Items")
            while LAST_EVALUATED_KEY in response:
                response = self.table.scan(
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )
                comics.append(response.get("Items"))

            for comic in comics:
                cleaned_comics.append(replace_decimals(comic))
            return cleaned_comics
        except ClientError as e:
            print(f"Exception")

    def get_comics_page(self, pagination_key_id: str) -> Dict:
        cleaned_comics = []
        print("getting comics")
        start_key = {'comicId': pagination_key_id}

        try:
            if pagination_key_id == "first":
                response = self.table.scan(
                    Limit=PAGE_LIMIT
                )
            else:
                response = self.table.scan(
                    ExclusiveStartKey=start_key,
                    Limit=PAGE_LIMIT
                )
            comics = response.get("Items")

            for comic in comics:
                cleaned_comics.append(replace_decimals(comic))

            return {
                "comics": cleaned_comics,
                "pageId": response.get(LAST_EVALUATED_KEY, {}).get("comicId")
            }
        except ClientError as e:
            print(f"Exception")


# needed to clean DynamoDbs weird decimal types from the data
def replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj


def print_exception(exception):
    print(f"Exception occurred {exception}")

