import json

MY_USERNAME = "Landon"


def get_all_comics_handler(event, context):
    """
    Get list of all comic metadata.

    Returns
    ------
    API Gateway Lambda Proxy Output Format: list

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    return {
        "statusCode": 200,
        "body": json.dumps([{
            "comicId": "firstComic1",
            "comic": {
                "title": "My First Comic",
                "panels": [
                    {
                        "author": MY_USERNAME,
                        "panelId": "firstPanel1",
                        "voteCount": 5,
                        "childPanels": [
                            generate_dummy_panel(MY_USERNAME, "secondPanel1", 2, [
                                generate_dummy_panel(MY_USERNAME, "thirdPanel1", 3, [
                                    generate_dummy_panel(MY_USERNAME, "fourthPanel1", 4, [])
                                ])
                            ]),
                            {
                                "author": MY_USERNAME,
                                "panelId": "secondPanel2",
                                "voteCount": 4,
                                "childPanels": [],
                            },
                        ],
                    },
                ],
            },
        },
            {
                "comicId": "comic2",
                "comic": {
                    "title": "My Second Comic",
                    "panels": [
                        {
                            "author": MY_USERNAME,
                            "panelId": "firstPanel1",
                            "voteCount": 5,
                            "childPanels": [
                                {
                                    "author": MY_USERNAME,
                                    "panelId": "secondPanel1",
                                    "voteCount": 2,
                                    "childPanels": [],
                                },
                                {
                                    "author": MY_USERNAME,
                                    "panelId": "secondPanel2",
                                    "voteCount": 4,
                                    "childPanels": [],
                                },
                            ],
                        },
                    ],
                },
            }]),
    }


def generate_dummy_panel(author, panel_id, vote_count, child_panels):
    return {
            "author": author,
            "panelId": panel_id,
            "voteCount": vote_count,
            "childPanels": child_panels,
        }
