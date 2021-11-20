from comic_table import ComicTable
import json
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)


comic_table = ComicTable()

def get_all_comics_handler(event, context):
    """
    Get list of all comic metadata.

    Returns
    ------
    API Gateway Lambda Proxy Output Format: list

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    page_id = event["pathParameters"].get("pageId", "first")
    print(f"Getting comic for page {page_id}.")
    page_response = comic_table.get_comics_page(page_num=0 if page_id == "first" else int(page_id))

    response = {
        "statusCode": 200,
        "body": json.dumps(page_response, default=str),
    }

    return response
