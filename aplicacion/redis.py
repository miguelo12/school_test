"""
redis client
"""
import redis

redis_client = redis.Redis(decode_responses=True, host='redis', port=6379, db=0)
