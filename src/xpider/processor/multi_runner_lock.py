from redis import Redis

class MultiRunnerLock:
    def __init__(self, spider:object):
        settings = spider.settings
        self.process_loop = spider.process_loop
        self.spider = spider
        redis_url = settings.get("redis_url")
        self.client = None
        if redis_url is not None:
            self.client = Redis.from_url(redis_url)
        
    def __enter__(self):
        if self.client is not None:
            if self.client.setnx("xpider_lock", 1):
                self.process_loop.process_results(self.spider.start_crawl())
        else:
            self.spider.logger.warning("No `redis_url` specified `Spider.start_crawl` will be invoked by multiple workers")
            self.process_loop.process_results(self.spider.start_crawl())
            
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if self.client is not None:
            self.client.delete("xpider_lock")
