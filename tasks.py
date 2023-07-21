from celery import Celery

app = Celery('hello', broker='redis://localhost')
app.conf.broker_url = 'redis://localhost:6379/0'


@app.task
def hello():
    return 'hello world'
