import json


def create_comic_handler(event, context):
    """
    Create new comic entry

    :return: The created comic meta data.
    """

    print(event)

    return {
        "statusCode": 200,
        "body": json.dumps({"comicId": "12345"}),
    }
