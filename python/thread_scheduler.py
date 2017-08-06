class PeriodicExecutor(threading.Thread):
    def __init__(self, interval, func, **kwargs):
        """ Execute func(params) every 'interval' seconds """
        threading.Thread.__init__(self, name="PeriodicExecutor")
        self.setDaemon(1)
        self._finished = threading.Event()
        self._interval = interval
        self._func = func
        self._params = kwargs
    
    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval
    
    def shutdown(self):
        """Stop this thread"""
        self._finished.set()
    
    def run(self):
        while 1:
            if self._finished.isSet(): return
            self._func(**self._params)
            # sleep for interval or until shutdown
            self._finished.wait(self._interval)

    def init_periodic_feedRefresh(self):
        self.feed_thread = dict()
        feeds_oneTimer=[]
        for feed in self.config.feeds:
            for name in feed:
                if not feed[name]['enabled']:
                    continue
                try:
                    refresh_time = feed[name]['refresh_delay']
                    self.feed_thread[name] = PeriodicExecutor(refresh_time, self.feed_refresh, feed=feed, name=name)
                    self.feed_thread[name].start()
                except KeyError:
                    feeds_oneTimer.append([feed, name])
        
        if feeds_oneTimer:
            refresh_time = self.config.network['default_refresh_delay']
            self.feed_thread["__oneTimer__"] = PeriodicExecutor(refresh_time, self.feed_refresh_oneTimer, feeds=feeds_oneTimer)
            self.feed_thread["__oneTimer__"].start()
