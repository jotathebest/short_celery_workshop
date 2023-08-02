import datetime
import logging
import time
from copy import deepcopy
from typing import Optional

import pytz

from celery import Celery

app = Celery("hello", broker="redis://localhost/0", backend="redis://localhost:6379")
app.conf.broker_transport_options = {'visibility_timeout': 30}  # 30 seconds.

logger = logging.getLogger(__name__)


def get_localized_now_with_pytz():
    now = datetime.datetime.now(tz=pytz.utc)
    return now


@app.task(
    name="my-task",
    retry_backoff=5,
    retry_kwargs={'max_retries': 1},
    queue="integrations",
    time_limit=120,  # 2 minutes,
    acks_late=True
)
def my_task(task_id):
    logger.info(f"Starting task with id {task_id}")
    time.sleep(40)
    logger.info(f"finished task with id {task_id}")


@app.task(
    name="handler-task",
    retry_backoff=5,
    retry_kwargs={'max_retries': 1},
    queue="integrations",
    time_limit=120,  # 2 minutes,
    acks_late=True
)
def handler(unique_task_id: str, start_date: datetime.datetime, timeout: int = 10):
    now = deepcopy(start_date)
    end = start_date + datetime.timedelta(seconds=timeout)
    task = my_task.delay(task_id=unique_task_id)

    while now < end and not task.ready():
        logger.info(f"waiting for handler to finish, it should finish at {end.isoformat()}")
        time.sleep(5)
        now = get_localized_now_with_pytz()

    while not task.ready():
        logger.info(f"waiting for task with id {unique_task_id} to finish, the end date should be {end.isoformat()}")
        time.sleep(5)

    logger.info(f"finished task with id {unique_task_id}")