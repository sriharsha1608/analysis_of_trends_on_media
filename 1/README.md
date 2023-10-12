
## Project Abstract

The usage of different platforms and the massive rise in the userbase and data consumption has led to the invention of Data crawlers. Data crawlers extract the data from the specified platform periodically or continuously depending on developer needs. These Data crawlers can also be used in further research activities. For e.g. the crawled data can be useful to other researchers in their studies. In this project, we are building a  Data crawler that extracts data from various social media platforms: Twitter, Reddit, and HackerNews. Collected data from the crawler is stored in a relational Database, PostgreSQL using an individual table for each platform.

## Tech-stack

* `python` - The project is developed and tested using python v3.8. [Python Website](https://www.python.org/)
* `request` - Request is a popular HTTP networking module(aka library) for python programming language. [Request Website](https://docs.python-requests.org/en/latest/#)
* `postgreSQL`- This project uses relationalDB postgreSQL for saving collected data. 
    * [PostgreSQL Website](https://www.postgresql.org/)
    * [Python PostgreSQL Adapter - psycopg2](https://www.psycopg.org/)

## Three data-source documentation

* `Twitter`
  * [Volume Stream API](https://api.twitter.com/2/tweets/sample/stream) - A regular 1% volume stream API from Twitter.
* `Reddit` - We are using `r/technology` 
  * [r/technology](https://reddit.com/r/technology) - Subreddit to discuss about latest happenings in Technology
  * [API-1](https://www.reddit.com/api/v1/access_token) - Reddit API requires users to obtain an access token before making queries
  * [API-2](https://oauth.reddit.com/api/v1/me) - Request a temporary OAuth token from Reddit
* `HackerNews` - Stories are Submitted by Authors, and Karma Points define user engagement
  * [API-Link](https://hacker-news.firebaseio.com/v0/item/) - It fetches latest stories posted on HN
  * [Website-link](https://news.ycombinator.com/) - HN is owned by Y-Combinator


## How to run the project?

Install `Python` and `PostgreSQL`

sudo apt install python3-pip
pip install psycopg2-binary
sudo apt-get install libpq-dev
pip3 install psycopg2
sudo apt install postgresql-client-common
sudo apt install postgresql-client
sudo apt install postgresql postgresql-contrib
sudo service postgresql start

sudo -i -u postgres

  createdb datadb \\creating database

  psql -d datadb \\to view this db
  alter user postgres password 'password'

  From Schema.txt, create the tables

  \d

  logout

set -a

source confing.env

set +a

run python3 filename.py \\ for running one file at a time

//bash run.sh
## Database schema - SQL 
***********************************************

table1_name: twitter_data

| id (pk) | content | author_id | created_at | users |
| ------ | ------ | ------ | ------ | ------ |  
| text | text | text | text | timestamp | text |

table2_name: reddit_data

| id (pk) | subreddit | title | selftext | upvote_ratio | ups | downs | score |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | 
| text | text | text | text | text | text | text | text |


table3_name: hn_stories

| id (pk) | by | descendants | score | time | title | url |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | 
| bigint | text | bigint | bigint | bigint | text | text |

## -----END----




