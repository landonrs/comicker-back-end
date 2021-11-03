import json

import pytest
import vote_on_comic
import common.okta_helper as okta_helper
from unittest.mock import MagicMock

SOME_OTHER_USER = "someOtherUser"
TEST_USER_ID = "testUserId"
TEST_USER_AUTH_HEADER = "Bearer testUserToken"
TEST_USER_PROFILE = {
    "sub": TEST_USER_ID
}

TEST_COMIC_ID = "firstComic1"
TEST_PANEL_2_ID = "secondPanel1"

TEST_BASIC_COMIC = {
    "lastUpdated": "2020-12-05T22:03:33.613021",
    "comicId": TEST_COMIC_ID,
    "comic": {
        "title": "My First Comic",
        "panels": [
            {
                "panelId": "firstPanel1",
                "voterIds": [SOME_OTHER_USER],
                "author": SOME_OTHER_USER,
                "childPanels": [
                    {
                        "panelId": TEST_PANEL_2_ID,
                        "voterIds": [SOME_OTHER_USER],
                        "author": SOME_OTHER_USER,
                        "childPanels": []
                    },
                ]
            }
        ]
    },
    "createDate": "2020-12-05T22:03:33.612995"
}


def mock_get_comic(comic_id):
    comic_mapping = {
        TEST_COMIC_ID: TEST_BASIC_COMIC
    }

    return comic_mapping[comic_id]


def mock_get_user_profile(auth_header):
    user_mapping = {
        TEST_USER_AUTH_HEADER: TEST_USER_PROFILE
    }

    return user_mapping[auth_header]


mock_table = MagicMock()
mock_table.get_comic.side_effect = mock_get_comic

@pytest.fixture(autouse=True)
def common_mocks(monkeypatch):
    mock_table.reset_mock()
    monkeypatch.setattr(vote_on_comic, "ComicTable", lambda: mock_table)
    monkeypatch.setattr(okta_helper, "get_user_profile", mock_get_user_profile)


TEST_EVENT = {
    "headers": {"Authorization": TEST_USER_AUTH_HEADER},
    "pathParameters": {"comicId": TEST_COMIC_ID},
    "body": json.dumps({
        "panelId": TEST_PANEL_2_ID
    })
}


def test_should_add_new_panel_to_comic_data():
    expected_payload = {
        "lastUpdated": "2020-12-05T22:03:33.613021",
        "comicId": TEST_COMIC_ID,
        "comic": {
            "title": "My First Comic",
            "panels": [
                {
                    "panelId": "firstPanel1",
                    "voterIds": [SOME_OTHER_USER],
                    "author": SOME_OTHER_USER,
                    "childPanels": [
                        {
                            "panelId": TEST_PANEL_2_ID,
                            "voterIds": [SOME_OTHER_USER, TEST_USER_ID],
                            "author": SOME_OTHER_USER,
                            "childPanels": []
                        },
                    ]
                }
            ]
        },
        "createDate": "2020-12-05T22:03:33.612995"
    }

    result = vote_on_comic.vote_on_comic_panel_handler(TEST_EVENT, None)

    mock_table.put_comic.assert_called_once_with(expected_payload)
    assert json.loads(result["body"]) == {"comicData": expected_payload}

