from typing import Tuple
from xpider.queue.base_queue import BaseQueue
from redis import Redis
import json
class RedisQue(BaseQueue):
    def __init__(self, settings:dict):
        redis_url:str = settings.get("redis_url", "")
        self.project_name = settings.get("name")
        self.client = Redis.from_url(redis_url)
        self.queue_key = f"xpider_{self.project_name}_queue"
        self.no_ack_key = f"xpider_{self.project_name}_no_ack"


    def acknowledge(self, id_str: str):
        self.client.srem(self.no_ack_key, id_str)

    def enqueue(self, obj: dict):
        self.client.lpush(self.queue_key ,json.dumps(obj))

    def dequeue(self) -> Tuple[str, dict]:
        item: dict = json.loads(self.client.lpop(self.queue_key))
        id_str = item.get("requestId", "")
        self.client.sadd(self.no_ack_key, id_str)
        return id_str, item

    def empty(self) -> bool:
        return self.client.llen(self.queue_key) == 0

    def has_unprocessed(self) -> bool:
        return self.client.scard(self.no_ack_key) > 0