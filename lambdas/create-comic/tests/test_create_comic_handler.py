import pytest
# from create_comic import create_comic_handler as test_model
from create_comic import find_panel


TEST_COMIC = {
  "lastUpdated": "2020-12-05T22:03:33.613021",
  "comicId": "firstComic1",
  "comic": {
    "title": "My First Comic",
    "panels": [
      {
        "panelId": "firstPanel1",
        "voteCount": 5,
        "author": "Landon",
        "childPanels": [
          {
            "panelId": "secondPanel1",
            "voteCount": 2,
            "author": "Landon",
            "childPanels": [
              {
                "panelId": "thirdPanel1",
                "voteCount": 3,
                "author": "Landon",
                "childPanels": [
                  {
                    "panelId": "fourthPanel1",
                    "voteCount": 4,
                    "author": "Landon",
                    "childPanels": []
                  }
                ]
              }
            ]
          },
          {
            "panelId": "secondPanel2",
            "voteCount": 4,
            "author": "Landon",
            "childPanels": []
          }
        ]
      }
    ]
  },
  "createDate": "2020-12-05T22:03:33.612995"
}


@pytest.fixture(autouse=True)
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": '{ "test": "body"}',
        "headers": {
            "Accept-Encoding": "gzip, deflate, sdch",
        }
    }


def test_lambda_handler(apigw_event, mocker):
    ret = find_panel(TEST_COMIC["comic"]["panels"], "secondPanel2")

    print(ret)

