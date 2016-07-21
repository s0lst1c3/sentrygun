import redis
import time

r = redis.StrictRedis()
pubsub = r.pubsub()
pubsub.psubscribe('*')
for msg in pubsub.listen():
    print 'test'
    print time.time(), msg
