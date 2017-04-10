# TweetTrend
6998 Project 2 TweetTrend  
Group 11  
Keyi Yang   UNI:ky2343   
Yunqing Jiang    UNI:yj2407   
  
- Frontend web page deployed by AWS Elastic Beanstalk and Django (related folder: Django).  
- Fetched tweets are stored by two methods (related folder: worker):  
>       Kafka: worker_kafka.py
>       Amazon Simple Queue Service: worker_sqs.py
- Included Natrual Language Understanding API by IBM to analyze tweets' content (related file: worker/natrual_reco.py)
- Used Amazon Simple Notification Service for workers to send the processed tweets to.
