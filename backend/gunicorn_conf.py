import multiprocessing

workers =  1 + multiprocessing.cpu_count() * 2
worker_class = "gevent"
errorlog = '-'
accesslog = '-'
timeout = 90