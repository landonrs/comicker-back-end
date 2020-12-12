import json
from common.comic_table import ComicTable
import common.okta_helper as okta_helper


def vote_on_comic_panel_handler(event, context):
    """
    Vote on a comic panel

    :return: The comic panel data.
    """

    print(event["pathParameters"])

    comic_id = event["pathParameters"].get("comicId")
    panel_id = event["body"].get("panelId")
    if not comic_id or not panel_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "missing required fields"}),
        }

    auth_header = event["headers"].get("Authorization", "")
    user_profile = okta_helper.get_user_profile(auth_header)
    if not user_profile:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "not authorized"}),
        }

    user_id = user_profile["sub"]

    comic_table = ComicTable()

    comic_data = comic_table.get_comic(comic_id)

    updated_comic = _add_user_to_panel_votes(comic_data, user_id, panel_id)

    comic_table.put_comic(updated_comic)

    return {
        "statusCode": 200,
        "body": json.dumps({"comicId": comic_id}),
    }


def _add_user_to_panel_votes(comic_data, user_id, panel_id):
    # TODO find panel and add user id to it
    return comic_data
