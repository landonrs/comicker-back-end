from common.comic_table import ComicTable
import json
MY_USERNAME = "Landon"


def get_all_comics_handler(event, context):
    """
    Get list of all comic metadata.

    Returns
    ------
    API Gateway Lambda Proxy Output Format: list

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    comics_list = ComicTable().get_comics()

    response = {
        "statusCode": 200,
        "body": json.dumps(comics_list),
    }

    print(response)

    return response


# def generate_dummy_panel(author, panel_id, vote_count, child_panels):
#     return {
#             "author": author,
#             "panelId": panel_id,
#             "voteCount": vote_count,
#             "childPanels": child_panels,
#         }

# if __name__ == '__main__':
#     get_all_comics_handler({}, {})