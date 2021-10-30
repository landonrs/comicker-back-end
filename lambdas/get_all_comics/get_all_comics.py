from common.comic_table import ComicTable
import json


def get_all_comics_handler(event, context):
    """
    Get list of all comic metadata.

    Returns
    ------
    API Gateway Lambda Proxy Output Format: list

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    page_id = event["pathParameters"].get("pageId", "first")
    page_response = ComicTable().get_comics_page(page_id)

    response = {
        "statusCode": 200,
        "body": json.dumps(page_response),
    }

    return response
