import pytest
import create_comic
import common.okta_helper as okta_helper
from unittest.mock import MagicMock
import uuid

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
                "voterIds": [TEST_USER_ID],
                "author": TEST_USER_ID,
                "childPanels": [
                    {
                        "panelId": TEST_PANEL_2_ID,
                        "voterIds": [TEST_USER_ID],
                        "author": TEST_USER_ID,
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

MOCK_UUID = "mockUUID"
MOCK_TIMESTAMP = "mockTimestamp"


@pytest.fixture(autouse=True)
def common_mocks(monkeypatch):
    mock_table.reset_mock()
    monkeypatch.setattr(create_comic, "ComicTable", lambda: mock_table)
    monkeypatch.setattr(okta_helper, "get_user_profile", mock_get_user_profile)
    monkeypatch.setattr(uuid, "uuid4", lambda: MOCK_UUID)
    monkeypatch.setattr(create_comic, "_get_timestamp", lambda: MOCK_TIMESTAMP)


TEST_EVENT = {
    "headers": {"Authorization": TEST_USER_AUTH_HEADER},
    "body": {
        "comicId": TEST_COMIC_ID,
        "parentPanelId": TEST_PANEL_2_ID
    }
}


def test_should_add_new_panel_to_comic_data():
    expected_payload = {
        "lastUpdated": MOCK_TIMESTAMP,
        "comicId": TEST_COMIC_ID,
        "comic": {
            "title": "My First Comic",
            "panels": [
                {
                    "panelId": "firstPanel1",
                    "voterIds": [TEST_USER_ID],
                    "author": TEST_USER_ID,
                    "childPanels": [
                        {
                            "panelId": TEST_PANEL_2_ID,
                            "voterIds": [TEST_USER_ID],
                            "author": TEST_USER_ID,
                            "childPanels": [
                                {
                                    "panelId": MOCK_UUID,
                                    "voterIds": [TEST_USER_ID],
                                    "author": TEST_USER_ID,
                                    "childPanels": []
                                }]
                        },
                    ]
                }
            ]
        },
        "createDate": "2020-12-05T22:03:33.612995"
    }

    create_comic.create_comic_handler(TEST_EVENT, None)

    mock_table.put_comic.assert_called_once_with(expected_payload)


NEW_COMIC_TITLE = "newComicTitle"
TEST_NEW_COMIC_EVENT = {
    "headers": {"Authorization": TEST_USER_AUTH_HEADER},
    "body": {
        "title": NEW_COMIC_TITLE,
    }
}


def test_should_create_new_comic():
    expected_payload = {
        "lastUpdated": MOCK_TIMESTAMP,
        "comicId": MOCK_UUID,
        "comic": {
            "title": NEW_COMIC_TITLE,
            "panels": [
                {
                    "panelId": MOCK_UUID,
                    "voterIds": [TEST_USER_ID],
                    "author": TEST_USER_ID,
                    "childPanels": []
                }
            ]
        },
        "createDate": MOCK_TIMESTAMP
    }

    create_comic.create_comic_handler(TEST_NEW_COMIC_EVENT, None)

    mock_table.put_comic.assert_called_once_with(expected_payload)