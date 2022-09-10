from typing import Dict, Tuple

LAST_UPDATED = "lastUpdated"

CREATE_DATE = "createDate"

PANELS = "panels"

TITLE = "title"

COMIC = "comic"

COMIC_ID = "comicId"


class Comic:

    def __init__(self, event: Dict):
        self.comic_id = event[COMIC_ID]
        self.title = event[COMIC][TITLE]
        self.panels = event[COMIC][PANELS]
        self.create_date = event[CREATE_DATE]
        self.last_updated = event[LAST_UPDATED]
