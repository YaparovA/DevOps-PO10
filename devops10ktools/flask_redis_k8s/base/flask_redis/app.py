import time
import redis
from flask import Flask, make_response
import socket
import os

DB_HOST = os.getenv('REDIS_HOST', 'redis')
MY_ENV = os.getenv('ENV', 'unknown')

app = Flask(__name__)
cache = redis.Redis(host=DB_HOST, port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! Yo! Yo! Yo! I have been seen {} times. My name is: {} My env: {}\n'.format(count, socket.gethostname(), MY_ENV)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
