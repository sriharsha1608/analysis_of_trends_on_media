import os
import time

import psycopg2
import requests


class PostgresConn:
    def __init__(self):
        self.user = os.environ.get("DATA_CAPTURE_POSTGRES_USER")
        self.password = os.environ.get("DATA_CAPTURE_POSTGRES_PWD")
        self.host = os.environ.get("DATA_CAPTURE_POSTGRES_HOST")
        self.port = os.environ.get("DATA_CAPTURE_POSTGRES_PORT")
        self.db = os.environ.get("DATA_CAPTURE_POSTGRES_DB_NAME")
        self.connection = None
        self.connect()

    def insert_data(self, storyDto):
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor()
            postgres_insert_query = """ INSERT INTO hn_stories (by, descendants, id, score, time, title, url) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"""
            record_to_insert = (
                storyDto.by, storyDto.descendants, storyDto.id, storyDto.score, storyDto.time, storyDto.title,
                storyDto.url)
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
            self.connection = psycopg2.connect(user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port,
                                               database=self.db)
            print("Connection est. with postgres")

        except (Exception, psycopg2.Error) as error:
            print("Unable to connect to db", error)


def get_url_prefix():
    return "https://hacker-news.firebaseio.com/v0/"


def get_new_story_ids():
    url = get_url_prefix() + "newstories.json"
    payload = {}
    headers = {}
    res = requests.get(url, headers=headers, data=payload)
    return res.json()


class StoryDto:
    def __init__(self, data):
        self.by = data.get("by", None)
        self.descendants = data.get("descendants", None)
        self.id = data.get("id", None)
        self.score = data.get("score", None)
        self.time = data.get("time", None)
        self.title = data.get("title", None)
        self.url = data.get("url", None)


def get_story(story_id):
    url = "https://hacker-news.firebaseio.com/v0/item/" + str(story_id) + ".json"
    res = requests.get(url, headers={}, data={})
    return StoryDto(res.json())


def insert_new_stories():
    global count
    ids = get_new_story_ids()
    ids.reverse()
    for story_id in ids[:5]:
        story = get_story(story_id)
        dbConn.insert_data(story)
        count = count + 1
        print('HackerNews: captured count', count)


dbConn = PostgresConn()
MAX_ENTRIES = 1000
SLEEP_INTERVAL_IN_SECS = 10
count = 0

while True:
    insert_new_stories()
    print('HackerNews: ' + "going to sleep for " + str(SLEEP_INTERVAL_IN_SECS) + " seconds")
    time.sleep(SLEEP_INTERVAL_IN_SECS)
    print('HackerNews: ' + "woke up from sleep")

print('HackerNews: ' + "fetched around " + str(MAX_ENTRIES) + " new stories data")
