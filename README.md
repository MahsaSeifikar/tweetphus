# tweetphus
A web interface to crawl users from Twitter platform in easy way.


To see the web interface, you just need to run the following command
``` docker-compose up --build ```

Then open the browser at http://0.0.0.0:8000


### How this version work?
In this version, you can upload a .pickle file containing a set of users' id, then when you click on the crawl button all follower and following of all the users will be crawled and saved in `/media` directory.