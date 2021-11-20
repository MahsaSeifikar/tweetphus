from __future__ import absolute_import, unicode_literals
import os
import logging
import pickle
import random
import tweepy
from django.conf import settings
from crawller.models import User

from .app import app as celery_service  

logger = logging.getLogger(__name__)


auth = tweepy.OAuthHandler(os.environ.get("CONSUMER_KEY", ""), os.environ.get("CONSUMER_SECRET", ""))
auth.set_access_token(os.environ.get("ACCESS_TOKEN", ""), os.environ.get("ACCESS_TOKEN_SECRET", ""))  
api = tweepy.API(auth, wait_on_rate_limit=True)

def crawl_user(user_id):
    sample_user = {"followers":[], "friends":[]}
    try:
        c = 0
        for follower in tweepy.Cursor(api.get_followers_id, user_id=user_id).items(50000):
            sample_user["followers"].extend(follower)
            c+= 1
        
        print(f"{c} pages ==> {user_id} followers: {len(sample_user['followers'])}")
        
        c = 0
        for friend in tweepy.Cursor(api.get_friends, user_id=user_id).items(50000):
            sample_user["friends"].extend(friend)
            c += 1
        print(f"{c} pages ==> {user_id} friends: {len(sample_user['friends'])}")
    except Exception as e:
        logger.error(e)

    try:
        path = os.path.join(settings.MEDIA_ROOT, "OCT/")
        # save in file
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(os.path.join(path, f"{user_id}.pickle"), "wb")
        pickle.dump(sample_user, f)

        # save in db
        user = User(user_id=f"{user_id}")
        user.save()
    except Exception as e:
        logger.error(e)
        

@celery_service.task(name="user_crawller", default_retry_delay=30 * 60, retry_backoff=5, retry_kwargs={'max_retries': 10, 'countdown': 10}, soft_time_limit=6000)
def user_queue(users_set):

    logger.error(f"{len(users_set)} users crawling is started!")
    for i, user in enumerate(users_set):
        if not i%101:
            logger.error(f"{i} user's following and followers are extract!")
        crawl_user(user)

    logger.error("crawling is finished!")

    return True