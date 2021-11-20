import json
from comic_table import ComicTable
import okta_helper as okta_helper
import comic_navigation as comic_nav
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

VOTER_IDS = "voterIds"


comic_table = ComicTable()

def vote_on_comic_panel_handler(event, context):
    """
    Vote on a comic panel

    :return: The comic panel data.
    """

    comic_id = event["pathParameters"].get("comicId")
    panel_id = json.loads(event["body"]).get("panelId")
    if not comic_id or not panel_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "missing required fields"}),
        }
    # Stupid API gateway lower cases the headers!!!
    # but sam local does not
    auth_header = event["headers"].get("authorization", None)
    if not auth_header:
        auth_header = event["headers"].get("Authorization", '')
    user_profile = okta_helper.get_user_profile(auth_header)
    if not user_profile:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "not authorized"}),
        }

    user_id = user_profile["sub"]

    comic_data = comic_table.get_comic(comic_id)

    panel = comic_nav.find_panel(comic_data["panels"], panel_id)
    if not panel:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "panel id not found in comic"}),
        }

    # don't let users vote multiple times
    if user_id not in panel[VOTER_IDS]:
        panel[VOTER_IDS].append(user_id)

    comic_table.update_comic(comic_data)

    return {
        "statusCode": 200,
        "body": json.dumps({"comicData": comic_data}, default=str),
    }
