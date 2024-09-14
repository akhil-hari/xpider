from xpider.queue.list_queue import ListQueue


class QueueFactory:
    @staticmethod
    def create_queue(queue_type: str = "default"):
        impl_map = {"default": ListQueue}
        return impl_map[queue_type]()
