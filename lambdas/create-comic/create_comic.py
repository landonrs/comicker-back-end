import json

from comic_table import ComicTable
from image_url_helper import ImageUrlHelper
import okta_helper as okta_helper
import comic_navigation as comic_nav
import uuid

SUB = "sub"
GIVEN_NAME = "given_name"

comic_table = ComicTable()


def create_comic_handler(event, context):
    """
    Create new comic entry, or add panel to existing comic

    :return: The created comic meta data.
    """
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

    body = json.loads(event["body"])

    comic_id = body.get("comicId")

    if comic_id:
        # comic was previously created, get from database and add panel
        print(f"updating existing comic {comic_id}.")
        comic_data = comic_table.get_comic(comic_id)
        parent_panel_id = body.get("parentPanelId")
        if not parent_panel_id:
            return return_400("missing required fields")

        new_panel = generate_panel(user_profile)
        parent_panel = comic_nav.find_panel(comic_data["panels"], parent_panel_id)

        if not parent_panel:
            return return_400("parent panel id does not exist in comic")

        parent_panel["childPanels"].append(new_panel)
        comic_table.update_comic(comic_data)
        url = ImageUrlHelper().create_put_object_presigned_url(object_key=f"comics/{comic_id}/{new_panel['panelId']}.jpg")

        return {
            "statusCode": 200,
            "body": json.dumps({"panelId": new_panel["panelId"], "imageUrl": url}),
        }
    else:
        comic_title = body["title"]
        print(f"creating new comic {comic_title}.")
        # creating new comic
        comic_id = _create_uuid()
        comic_id_response = _create_new_comic(user_profile, comic_title, comic_id)
        url = ImageUrlHelper().create_put_object_presigned_url(object_key=f"comics/{comic_id}/{comic_id}.jpg")
        comic_id_response.update({"imageUrl": url})

        return {
            "statusCode": 200,
            "body": json.dumps(comic_id_response),
        }


def generate_panel(user_profile, panel_id=None):
    return {
                    "panelId": panel_id if panel_id else _create_uuid(),
                    "voterIds": [user_profile[SUB]],
                    # storing the actual user's name for the alpha, to make things much simpler
                    # this will be removed if I ever get into a beta phase
                    "author": user_profile[GIVEN_NAME],
                    "authorId": user_profile[SUB],
                    "childPanels": []
                }


def _create_new_comic(user_profile, comic_title, comic_id):
    comic_data = {
        "comicId": comic_id,
        "title": comic_title,
        "panels": [
            generate_panel(user_profile, comic_id)
        ]}

    ComicTable().create_comic(comic_data)

    return {"comicId": comic_id}


def _create_uuid():
    return str(uuid.uuid4())


def return_400(message):
    return {
                "statusCode": 400,
                "body": json.dumps({"message": message}),
            }