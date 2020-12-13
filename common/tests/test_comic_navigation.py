import comic_navigation
import pytest

TEST_PANEL_ID_1 = "testPanel1"
TEST_PANEL_ID_2 = "testPanel2"
TEST_PANEL_ID_3 = "testPanel3"
TEST_PANEL_ID_4 = "testPanel4"
TEST_PANEL_ID_5 = "testPanel5"
TEST_PANEL_ID_6 = "testPanel6"
TEST_PANEL_ID_7 = "testPanel7"
TEST_PANEL_ID_8 = "testPanel8"
PANEL_LIST = [TEST_PANEL_ID_1, TEST_PANEL_ID_2, TEST_PANEL_ID_3, TEST_PANEL_ID_4, TEST_PANEL_ID_5, TEST_PANEL_ID_6,
              TEST_PANEL_ID_7, TEST_PANEL_ID_8]
TEST_COMIC_PANELS = [
    {
        "panelId": TEST_PANEL_ID_1,
        "voterIds": [],
        "author": "test",
        "childPanels": [
            {
                "panelId": TEST_PANEL_ID_2,
                "voterIds": [],
                "author": "test",
                "childPanels": [
                    {
                        "panelId": TEST_PANEL_ID_8,
                        "voterIds": [],
                        "author": "test",
                        "childPanels": []
                    }
                ]
            },
            {
                "panelId": TEST_PANEL_ID_3,
                "voterIds": [],
                "author": "test",
                "childPanels": [
                    {
                        "panelId": TEST_PANEL_ID_4,
                        "voterIds": [],
                        "author": "test",
                        "childPanels": [
                            {
                                "panelId": TEST_PANEL_ID_5,
                                "voterIds": [],
                                "author": "test",
                                "childPanels": []
                            },
                            {
                                "panelId": TEST_PANEL_ID_6,
                                "voterIds": [],
                                "author": "test",
                                "childPanels": []
                            },
                            {
                                "panelId": TEST_PANEL_ID_7,
                                "voterIds": [],
                                "author": "test",
                                "childPanels": []
                            }
                        ]
                    }]
            }
        ]
    }]


@pytest.mark.parametrize("mock_panel_ids", PANEL_LIST)
def test_should_find_panels(mock_panel_ids):
    result = comic_navigation.find_panel(TEST_COMIC_PANELS, mock_panel_ids)

    assert result is not None


def test_should_return_none_if_panel_not_found():
    result = comic_navigation.find_panel(TEST_COMIC_PANELS, "bad_panel_id")

    assert result is None
