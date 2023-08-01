import datetime
import logging
import time
import pytz

from celery import Celery

app = Celery("hello", broker="redis://localhost")
app.conf.broker_url = "redis://localhost:6379/0"

logger = logging.getLogger(__name__)


def get_localized_now():
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    return now


def get_localized_now_with_pytz():
    now = datetime.datetime.now(tz=pytz.utc)
    return now


@app.task
def timer(task_id: str, timeout: int = 10):
    logger.info(f"Starting task with id {task_id}")
    now = get_localized_now_with_pytz()
    end = now + datetime.timedelta(seconds=timeout)
    while now < end:
        logger.info(f"waiting for {task_id} to finish, it should finish at {end.isoformat()}")
        time.sleep(5)
        now = get_localized_now_with_pytz()
    logger.info(f"finished task with id {task_id}")
