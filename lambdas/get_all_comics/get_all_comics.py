import json


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
                        "userId": "00u11x54p97nIxyef5d6",
                        "panelId": "firstPanel1",
                        "voteCount": 5,
                        "childPanels": [
                            {
                                "userId": "00u11x54p97nIxyef5d6",
                                "panelId": "secondPanel1",
                                "voteCount": 2,
                                "childPanels": [],
                            },
                            {
                                "userId": "00u11x54p97nIxyef5d6",
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
                            "userId": "00u11x54p97nIxyef5d6",
                            "panelId": "firstPanel1",
                            "voteCount": 5,
                            "childPanels": [
                                {
                                    "userId": "00u11x54p97nIxyef5d6",
                                    "panelId": "secondPanel1",
                                    "voteCount": 2,
                                    "childPanels": [],
                                },
                                {
                                    "userId": "00u11x54p97nIxyef5d6",
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
