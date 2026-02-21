from flask import Flask, request
from prometheus_client import Counter, Histogram, generate_latest
import time
import random

app = Flask(__name__)

# Define metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('app_request_duration_seconds', 'Request duration')
USER_SIGNUPS = Counter('app_user_signups_total', 'Total user signups')

@app.route('/')
def home():
    start = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=200).inc()
    time.sleep(random.uniform(0.1, 0.5))
    REQUEST_DURATION.observe(time.time() - start)
    return 'Hello, Monitoring World!'

@app.route('/signup', methods=['POST'])
def signup():
    USER_SIGNUPS.inc()
    REQUEST_COUNT.labels(method='POST', endpoint='/signup', status=201).inc()
    return 'User signed up!', 201

@app.route('/error')
def error():
    REQUEST_COUNT.labels(method='GET', endpoint='/error', status=500).inc()
    return 'Error!', 500

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)