import decimal

import boto3
from botocore.exceptions import ClientError
from datetime import datetime


"""
REALLY JANKY, but REMEMBER TO COPY THIS INTO EVERY LAMBDA DIRECTORY WHEN DONE DEVELOPING!!!
"""

TABLE_NAME = "comicTable"
LOCAL_ENDPOINT = "http://dynamo:8000"
LAST_EVALUATED_KEY = "LastEvaluatedKey"


class ComicTable:
    def __init__(self):
        self.table = boto3.session.Session().resource('dynamodb', endpoint_url=LOCAL_ENDPOINT).Table(
            TABLE_NAME)

    def put_comic(self, comic_data):
        last_updated_timestamp = datetime.utcnow().isoformat()
        comic_data.update({"lastUpdated": last_updated_timestamp})
        try:
            response = self.table.put_item(
                Item=comic_data
            )
            return response
        except ClientError as e:
            print(f"Exception occurred {e}")

    def create_comic(self, comic_data):
        # record create time
        create_time_stamp = datetime.utcnow().isoformat()
        comic_data["createDate"] = create_time_stamp

        return self.put_comic(comic_data)

    def get_comics(self, pagination_key = None, sort_type = None):
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


def bootstrap_table():
    comic_table = ComicTable()
    comic_table.create_comic({
        "comicId": "firstComic1",
        "comic": {
            "title": "My First Comic",
            "panels": [
                {
                    "author": "Landon",
                    "panelId": "firstPanel1",
                    "voteCount": 5,
                    "childPanels": [
                        {
                            "author": "Landon",
                            "panelId": "secondPanel1",
                            "voteCount": 2,
                            "childPanels": [
                                {
                                    "author": "Landon",
                                    "panelId": "thirdPanel1",
                                    "voteCount": 3,
                                    "childPanels": [
                                        {
                                            "author": "Landon",
                                            "panelId": "fourthPanel1",
                                            "voteCount": 4,
                                            "childPanels": []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "author": "Landon",
                            "panelId": "secondPanel2",
                            "voteCount": 4,
                            "childPanels": []
                        }
                    ]
                }
            ]
        }
    })


def read_comics():
    comic_table = ComicTable()
    print(comic_table.get_comics())

if __name__ == '__main__':
    # bootstrap_table()
    read_comics()