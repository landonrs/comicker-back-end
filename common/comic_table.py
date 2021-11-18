import json
from typing import Dict
import os
import boto3
import psycopg2 as pg
import psycopg2.extras


TABLE_NAME = "comicTable"
LOCAL_ENDPOINT = "localhost"
PROD_ENDPOINT = "comickerdb.cz7ocvnyxvk3.us-east-1.rds.amazonaws.com"

DB_PARAMETER = "comicker-db-creds"
LAST_EVALUATED_KEY = "LastEvaluatedKey"
PAGE_LIMIT = 10


class ComicTable:
    def __init__(self):
        try:
            if os.getenv("SYSTEM") == "prod":
                ssm_client = boto3.client("ssm")
                db_creds = json.loads(ssm_client.get_parameter(Name=DB_PARAMETER)["Parameter"]["Value"])
                conn = pg.connect(
                    f"dbname='comicker' user={db_creds['user']} host={PROD_ENDPOINT} password={db_creds['password']}")

            else:
                conn = pg.connect(
                    f"dbname='comicker' user='docker' host={LOCAL_ENDPOINT} password='docker'")

            conn.set_session(autocommit=True)
            self.cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except Exception as e:
            print(f"unable to connect to the database {repr(e)}")

    def get_comic(self, comic_id):
        try:
            query = f"""SELECT *
                        FROM comic
                        WHERE comic."comicId" = '{comic_id}';
                    """

            self.cursor.execute(query)

            comics = self.cursor.fetchall()
            # TODO - remove once front end is using new contract
            for comic in comics:
                comic.update({"comic": {"title": comic["title"], "panels": comic["panels"]}})

            return comics[0]
        except Exception as e:
            print_exception(e)
            return None

    def create_comic(self, comic_data) -> None:
        try:
            self.cursor.execute(f"""INSERT INTO comic VALUES ('{comic_data['comicId']}', '{comic_data['title']}', '{json.dumps(comic_data['panels'])}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);""")
        except Exception as e:
            print_exception(e)
            raise e

    def update_comic(self, comic_data) -> None:
        try:
            query = f"""UPDATE comic
                        SET panels = '{json.dumps(comic_data["panels"])}',
                            "lastUpdated" = CURRENT_TIMESTAMP
                        WHERE "comicId" = '{comic_data["comicId"]}';
                        COMMIT;"""
            self.cursor.execute(query)
        except Exception as e:
            print_exception(e)
            raise e

    def get_comics_page(self, page_num: int) -> Dict:
        print("getting comics")

        offset = page_num * PAGE_LIMIT

        try:
            query = f"""SELECT *
               FROM comic
               ORDER BY comic."lastUpdated" ASC
               LIMIT {PAGE_LIMIT}
               OFFSET {offset};
               """

            self.cursor.execute(query)

            comics = self.cursor.fetchall()
            # TODO - remove once front end is using new contract
            for comic in comics:
                comic.update({"comic": {"title": comic["title"], "panels": comic["panels"]}})

            return {
                "comics": comics,
                "pageId": page_num + 1
            }
        except Exception as e:
            print_exception(e)


def print_exception(exception):
    print(f"Exception occurred {exception}")


# if __name__ == "__main__":
    # comic_table = ComicTable()
    # comic_table.create_comic({"comicId": "12345fsef", "title": "why?", "panels": json.dumps([{"key": "value"}])})
    # result = comic_table.get_comic("12345fsef")
    # result = comic_table.get_comics_page(0)
    # print(json.dumps(result, default=str))
