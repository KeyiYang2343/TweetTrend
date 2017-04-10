import boto3
from natural_reco import Analysis
import json
from multiprocessing import Pool
import pykafka

sns = boto3.resource('sns')
topic = sns.create_topic(Name='notification_tweet')
api_link = "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze"

client = pykafka.KafkaClient(hosts="34.205.9.40:9092")
topic_kafka = client.topics['test']
consumer = topic_kafka.get_simple_consumer(queued_max_messages = 10)

if __name__ == '__main__':
	consumer.start()
	for message in consumer:
		if message is not None:
			tweet = message.value
			print tweet
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

				print encoded
