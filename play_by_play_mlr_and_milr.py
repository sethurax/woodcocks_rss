import praw
from dhooks import Webhook
import datetime
import time
from os import getenv

subreddit = getenv('SUBREDDIT')
search_term = 'Williamsport Woodcocks'
webhook = Webhook(getenv('WEBHOOK'))
reddit_client_id = getenv('REDDIT_CLIENT_ID')
reddit_client_secret = getenv('REDDIT_CLIENT_SECRET')

reddit = praw.Reddit(
    client_id = reddit_client_id,
    client_secret = reddit_client_secret,
    user_agent = 'sethurax'
)

def parse_comments():
    for comment in reddit.subreddit(subreddit).stream.comments(skip_existing=True):
        update = '**/u/%s on [%s](<https://www.reddit.com%s>)**' % (comment.author, comment.link_title, comment.permalink)
        update += '```%s```' % comment.body
        update += '*Created at %s*' % (datetime.datetime.fromtimestamp(comment.created))
        if search_term.lower() in comment.link_title.lower():
            webhook.send(update)

while True:
    try:
        parse_comments()
    except Exception as e:
        print(e)
        time.sleep(60)
    else:
        time.sleep(360)
