import requests
import psycopg2
import os


class PostgresConn:

    def __init__(self):
        self.user = os.environ.get("DATA_CAPTURE_POSTGRES_USER")
        self.password = os.environ.get("DATA_CAPTURE_POSTGRES_PWD")
        self.host = os.environ.get("DATA_CAPTURE_POSTGRES_HOST")
        self.port = os.environ.get("DATA_CAPTURE_POSTGRES_PORT")
        self.db = os.environ.get("DATA_CAPTURE_POSTGRES_DB_NAME")
        self.connection = None
        self.connect()

    def insert_data(self, dto):
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor()
            postgres_insert_query = """ INSERT INTO reddit_data (id, subreddit, title, selftext, upvote_ratio, ups, downs, score) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"""
            record_to_insert = (
                dto.subreddit, dto.title, dto.selftext, dto.upvote_ratio, dto.ups, dto.downs, dto.score)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into reddit_data table", error)
        finally:
            if self.connection:
                cursor.close()

    def connect(self):
        try:
            self.connection = psycopg2.connect(user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port,
                                               database=self.db)
            print("Connection est. with postgres")

        except (Exception, psycopg2.Error) as error:
            print("Unable to connect to db", error)


class RedditDto:

    def __init__(self, _post):
        self.id = _post['data']['id']
        self.subreddit = _post['data']['subreddit']
        self.title = _post['data']['title']
        self.selftext = _post['data']['selftext']
        self.upvote_ratio = _post['data']['upvote_ratio']
        self.ups = _post['data']['ups']
        self.downs = _post['data']['downs']
        self.score = _post['data']['score']


auth = requests.auth.HTTPBasicAuth(os.environ.get("DATA_CAPTURE_REDDIT_CLIENT_ID"),
                                   os.environ.get("DATA_CAPTURE_REDDIT_SECRET"))

data = {'grant_type': 'password', 'username': os.environ.get("DATA_CAPTURE_REDDIT_USER"), 'password': os.environ.get("DATA_CAPTURE_REDDIT_PWD")}
headers = {'User-Agent': 'MyBot/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}


def insert_new_data():
    global collected_count
    res = requests.get("https://oauth.reddit.com/r/technology/new", headers=headers)
    for post in res.json()['data']['children']:
        redditDto = RedditDto(post)
        postgresConn.insert_data(redditDto)
        collected_count += 1
        print('Reddit: captured count', collected_count)


collected_count = 0
MAX_ENTRIES = 25
SLEEP_INTERVAL_IN_SECONDS = 10

postgresConn = PostgresConn()

while True:
    insert_new_data()
