from comic_table import ComicTable
import json
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)


def get_comic_handler(event, context):
    """
    Get comic associated with specified id

    Returns comic data
    """

    comic_id = event["pathParameters"]["comicId"]
    comic_response = ComicTable().get_comic(comic_id)

    if comic_response is None:
        response = {
            "statusCode": 404,
            "body": json.dumps({"message": "comic not found"}),
        }
    else:
        response = {
            "statusCode": 200,
            "body": json.dumps(comic_response),
        }

    return response
