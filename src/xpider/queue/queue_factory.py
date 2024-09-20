from xpider.queue.list_queue import ListQueue
from xpider.queue.redis_queue import RedisQue


class QueueFactory:
    @staticmethod
    def create_queue(settings:dict):
        queue_type = "default"
        queue_type = "redis" if settings.get("redis_url") is not None else queue_type
        impl_map = {
            "redis": RedisQue,
            "default": ListQueue
            }
        return impl_map[queue_type](settings)
