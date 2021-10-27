import json
from common.comic_table import ComicTable
import common.okta_helper as okta_helper
import common.comic_navigation as comic_nav

VOTER_IDS = "voterIds"


def vote_on_comic_panel_handler(event, context):
    """
    Vote on a comic panel

    :return: The comic panel data.
    """

    print(event["pathParameters"])

    comic_id = event["pathParameters"].get("comicId")
    panel_id = json.loads(event["body"]).get("panelId")
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

    panel = comic_nav.find_panel(comic_data["comic"]["panels"], panel_id)
    if not panel:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "panel id not found in comic"}),
        }

    # don't let users vote multiple times
    if user_id not in panel[VOTER_IDS]:
        panel[VOTER_IDS].append(user_id)

    comic_table.put_comic(comic_data)

    return {
        "statusCode": 200,
        "body": json.dumps({"comicId": comic_id}),
    }
