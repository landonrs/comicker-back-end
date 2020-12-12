import json
from common.comic_table import ComicTable
import common.okta_helper as okta_helper
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
        # TODO add panel to parent
        return {
            "statusCode": 200,
            "body": json.dumps({"comicId": comic_id}),
        }

    else:
        comic_title = body["title"]
        # creating new comic
        comic_id_response = _create_new_comic(user_profile, comic_title)
        return {
            "statusCode": 200,
            "body": json.dumps(comic_id_response),
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
                    "vote_count": 0,
                    "voter_ids": [user_profile[SUB]],
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
