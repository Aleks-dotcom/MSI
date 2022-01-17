import redis
import os 
def get_connection():
	try:
		url  = os.environ['REDIS_URL']
		port  = os.environ['REDIS_PORT']
		r = redis.StrictRedis(host=url, port=port, password="", decode_responses=True)
		print(f"Redis connection succeeded: {r}")
		return r
	except Exception as e:
		print(e)
		return -1
