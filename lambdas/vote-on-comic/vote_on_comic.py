import json


def vote_on_comic_panel_handler(event, context):
    """
    Vote on a comic panel

    :return: The comic panel data.
    """

    print(event["pathParameters"])

    return {
        "statusCode": 200,
        "body": json.dumps({"comicId": "12345"}),
    }
