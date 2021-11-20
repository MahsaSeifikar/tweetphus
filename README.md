# tweetphus
A web interface to crawl users from Twitter platform in easy way.

### How run this code?

1. Go to the `.env` folder create .tweepy file and copy the following variables then replace * with your twitter developer information.
```
CONSUMER_KEY="*"
CONSUMER_SECRET="*"
ACCESS_TOKEN="*"
ACCESS_TOKEN_SECRET="*"
```
2. Go to the main folder and run the following command

``` docker-compose up --build ```

3. Open the browser at http://0.0.0.0:8000


### How this version work?
In this version, you can upload a .pickle file containing a set of users' id, then when you click on the crawl button all follower and following of all the users will be crawled and saved in `/media` directory.
