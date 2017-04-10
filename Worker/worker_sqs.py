import boto3
from natural_reco import Analysis
import json
from multiprocessing import Pool

sqs = boto3.resource('sqs')
sns = boto3.resource('sns')
topic = sns.create_topic(Name='notification_tweet')
queue = sqs.get_queue_by_name(QueueName='tweets')
api_link = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze"
def worker(_):
	while 1:
		for message in queue.receive_messages(MaxNumberOfMessages=10,WaitTimeSeconds=15):
			try:
				tweet = message.body
				tweet = json.loads(tweet)
				content = tweet['text'].encode("utf-8")
				p = Analysis(content,api_link)
				res = p.request_api()
				decoded = json.loads(res)
				if decoded.has_key('sentiment'):
					attitude = decoded['sentiment']['document']['label']
					tweet['sentiment'] = attitude
					encoded = json.dumps(tweet, ensure_ascii=False)
					topic.publish(Message=encoded)
			finally:
				message.delete()


if __name__ == '__main__':
	pool = Pool(3)
	pool.map(worker,range(3))