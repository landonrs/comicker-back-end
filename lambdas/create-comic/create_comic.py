import json
from common.comic_table import ComicTable
import common.okta_helper as okta_helper
import common.comic_navigation as comic_nav
import uuid
from datetime import datetime

SUB = "sub"


def create_comic_handler(event, context):
    """
    Create new comic entry, or add panel to existing comic

    :return: The created comic meta data.
    """
    auth_header = event["headers"].get("Authorization", "")
    user_profile = okta_helper.get_user_profile(auth_header)
    if not user_profile:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "not authorized"}),
        }

    body = event["body"]
    comic_table = ComicTable()

    comic_id = body.get("comicId")

    if comic_id:
        # comic was previously created, get from database and add panel
        comic_data = comic_table.get_comic(comic_id)
        print(comic_data)
        parent_panel_id = body.get("parentPanelId")
        if not parent_panel_id:
            return return_400("missing required fields")

        new_panel = generate_panel(user_profile)
        parent_panel = comic_nav.find_panel(comic_data["comic"]["panels"], parent_panel_id)

        if not parent_panel:
            return return_400("parent panel id does not exist in comic")

        parent_panel["childPanels"].append(new_panel)
        comic_table.put_comic(comic_data)

        return {
            "statusCode": 200,
            "body": json.dumps({"panelId": new_panel["panelId"]}),
        }
    else:
        comic_title = body["title"]
        # creating new comic
        comic_id_response = _create_new_comic(user_profile, comic_title)
        return {
            "statusCode": 200,
            "body": json.dumps(comic_id_response),
        }


def generate_panel(user_profile):
    return {
                    "panelId": _create_uuid(),
                    "voterIds": [user_profile[SUB]],
                    "author": user_profile[SUB],
                    "childPanels": []
                }


def _create_new_comic(user_profile, comic_title):
    create_date = datetime.utcnow().isoformat()
    comic_id = _create_uuid()

    comic_data = {
        "createDate": create_date,
        "lastUpdated": create_date,
        "comicId": comic_id,
        "comic": {
            "title": comic_title,
            "panels": [
                {
                    "panelId": _create_uuid(),
                    "voterIds": [user_profile[SUB]],
                    "author": user_profile[SUB],
                    "childPanels": []
                }
            ]
        }}

    response = ComicTable().put_comic(comic_data)
    print(response)

    return {"comicId": comic_id}


def _create_uuid():
    return str(uuid.uuid4())


def return_400(message):
    return {
                "statusCode": 400,
                "body": json.dumps({"message": message}),
            }