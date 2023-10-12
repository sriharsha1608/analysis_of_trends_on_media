## Project Abstract

 Our aim is to do an analysis of trends in three different social media platforms i.e Twitter, Reddit, and HackerNews. Twitter and Reddit are high-scale social media platforms with an impeccable holding of users considering them as experts whereas HackerNews is at the start of the game evaluating them as beginners. Immediately after the selection of our three datasets, we started crawling data from each of the platforms by building a data crawler that extracts the data from the specified platform periodically or continuously depending on developer needs. Collected data from the crawler is stored in a relational Database, PostgreSQL using an individual table for each platform. Vectorization and k-means clustering are two important techniques used in the field of measurement and data analysis. K-means clustering is a machine learning algorithm that is used to group data points into clusters based on their similarity. Vectorization, on the other hand involves converting text or other non-numeric data into numerical vectors, which can then be used as input to machine learning algorithms.

## Tech-stack

* `python` - The project is developed and tested using python v3.8. [Python Website](https://www.python.org/)
* `request` - Request is a popular HTTP networking module(aka library) for python programming language. [Request Website](https://docs.python-requests.org/en/latest/#)
* `postgreSQL`- This project uses relationalDB postgreSQL for saving collected data. 
    * [PostgreSQL Website](https://www.postgresql.org/)
    * [Python PostgreSQL Adapter - psycopg2](https://www.psycopg.org/)
* `pandas` & `matplotlib` - Pandas and Matplotlib is not being used in actual crawler. It is being used just for collected data analysis.
* `Dash` - Dash is an open source framework for building data visualization interfaces.
* `Vader` - is a model used for text sentiment analysis that is sensitive to both polarity (positive/negative) and intensity (strength) of emotion.
* `NLTK`
* `Word Cloud`
* `Plotly`

## Techniques

 * `Vectorization` - Vectorization involves converting data, such as text or images, into a numerical vector representation, which can then be used in mathematical operations and algorithms.

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
Used Plotly module to represent the data in visual format.

To run this project, you will need to have Python and several libraries installed, including `NumPy`, `Pandas`,`wordcloud`,`Scikit-learn`,`Nltk`, `Dash`, `Plotly` and `Vader`.

The data collected from the three social media platforms (HackerNews, Twitter, and Reddit)in DB exported to csv format, so that it can be read by the Python pandas code easily.

Run the project by executing the Python code in a suitable environment, such as a `Jupyter notebook` or the `Python interactive shell`.

The code will pre-process the data, apply the TF-IDF representation and visualize and analyze the results.


## -----END----



