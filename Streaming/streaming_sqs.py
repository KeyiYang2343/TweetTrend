import json
import time
from codecs import open
from dateutil import parser
import tweepy
import boto3

consumer_key = 'ylY13IOjpXr7SOfjHKwsi0B5q'
consumer_secret = '5nFY7ulbZHKRzWbKxmqnyI0nGevgxrHuIvLDm16Nh6YhhErdQd'
access_token = '765007753467363328-h66wqYE0pq4iL5fbDpLhtkKOiMJSA89'
access_token_secret = 'bM3krkwgOK2pgnZV3iKjmiPnoorYMm2EYfV45JrsecVIA'

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='NewTwitt')

def appendlog(f, s):
    f.write(u'[{0}] {1}\n'.format(time.strftime('%Y-%m-%dT%H:%M:%SZ'), s))
    f.flush()

class TwittMapListener(tweepy.StreamListener):
    def __init__(self,f):
        super(TwittMapListener, self).__init__()
        self.f = f

    def on_data(self, data):
        # The tweets are retrieved only if the geolocation is tagged
        try:
            # Reference: https://dev.twitter.com/overview/api/tweets
            decoded = json.loads(data)
            geo = decoded.get('place')
            lang = decoded.get('lang')
            if lang == 'en' and geo is not None:
                # Parse geolocation from coordinates
                cord = geo['bounding_box']['coordinates'][0][0]
                timestamp = parser.parse(decoded['created_at'])
                timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
                tweet = {
                    'user': decoded['user']['screen_name'],
                    'text': decoded['text'],
                    'geo': cord,
                    'time': timestamp
                }
                tweet_id = decoded['id_str']
                appendlog(self.f, u'{0}: {1}'.format(tweet_id, json.dumps(tweet, ensure_ascii=False)))
                encoded = json.dumps(tweet, ensure_ascii=False)
                queue.send_message(MessageBody=encoded)
        except Exception as e:
            appendlog(self.f, '{0}: {1}'.format(type(e), str(e)))

    def on_error(self, status):
        if status == 420:  # Rate limited
            appendlog(self.f, 'Error 420')
            return False


if __name__ == '__main__':
    with open('streaming.log', 'a', encoding='utf8') as f:
        appendlog(f, 'Program starts')
        
        ls = TwittMapListener(f)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = tweepy.Stream(auth, ls)
        stream.filter(track=["Trump", "Hillary", "Hello", "Facebook", "LinkedIn",
                             "Amazon", "Google", "Uber", "Columbia", "New York"])





