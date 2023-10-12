import requests
import os
import json
import psycopg2

bearer_token = os.environ.get("DATA_CAPTURE_TWITTER_BEARER")


class UserDto:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.username = data["username"]
        self.created_at = data["created_at"]


class TwitterTweetDto:

    def __init__(self, data, users):
        self.id = data["id"]
        self.content = data["text"]
        self.author_id = data["author_id"]
        self.created_at = data["created_at"]
        self.users = users


class PostgresConn:

    def __init__(self):
        self.user = os.environ.get("DATA_CAPTURE_POSTGRES_USER")
        self.password = os.environ.get("DATA_CAPTURE_POSTGRES_PWD")
        self.host = os.environ.get("DATA_CAPTURE_POSTGRES_HOST")
        self.port = os.environ.get("DATA_CAPTURE_POSTGRES_PORT")
        self.db = os.environ.get("DATA_CAPTURE_POSTGRES_DB_NAME")
        self.connection = None
        self.connect()

    def insert_data(self, tweetDto):
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor()
            postgres_insert_query = """ INSERT INTO twitter_data (id, content, author_id, created_at, users) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"""
            record_to_insert = (
                tweetDto.id, tweetDto.content, tweetDto.author_id, tweetDto.created_at, json.dumps(tweetDto.users))
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)
        finally:
            # closing database connection.
            if self.connection:
                cursor.close()

    def connect(self):
        try:
            print(self.user, self.password)
            self.connection = psycopg2.connect(user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port,
                                               database=self.db)
            print("Connection est. with postgres")

        except (Exception, psycopg2.Error) as error:
            print("Unable to connect to db", error)


def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream" \
           + "?tweet.fields=created_at&expansions=author_id&user.fields=created_at"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r


def connect_to_endpoint(url):
    dbConn = PostgresConn()
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)
    print(response.status_code)
    collected_count = 0
    for response_line in response.iter_lines():
        if response_line:
            json_line = json.loads(response_line)
            json_data = json.loads(response_line)["data"]
            users = []
            if ("includes" in json_line) and ("users" in json_line["includes"]):
                json_users = json_line["includes"]["users"]
            data = TwitterTweetDto(json_data, json_users)
            dbConn.insert_data(data)
            collected_count += 1
            print('Twitter: captured count', collected_count)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )


def main():
    url = create_url()
    timeout = 0
    while True:
        connect_to_endpoint(url)
        timeout += 1


if __name__ == "__main__":
    main()
