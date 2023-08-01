import datetime
import logging
import time

from celery import Celery

app = Celery("hello", broker="redis://localhost")
app.conf.broker_url = "redis://localhost:6379/0"

logger = logging.getLogger(__name__)


@app.task
def timer(task_id: str, timeout: int = 10):
    logger.info(f"Starting task with id {task_id}")
    now = datetime.datetime.utcnow()
    end = now + datetime.timedelta(seconds=timeout)
    while now < end:
        logger.info(f"waiting for {task_id} to finish, it should finish at {end.isoformat()}")
        time.sleep(5)
        now = datetime.datetime.utcnow()
    logger.info(f"finished task with id {task_id}")
