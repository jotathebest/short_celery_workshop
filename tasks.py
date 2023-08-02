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


def has_reached_visibility_timeout(start_time: datetime.datetime, visibility_timeout: Optional[int] = None):
    # checks if we should stop the task as its execution time is close to the visibility timeout in order
    # to avoid the task being picked up by another worker
    visibility_timeout = app.conf.broker_transport_options.get(
        'visibility_timeout', 3600
    ) if visibility_timeout is None else visibility_timeout
    # minimal delta should be at least 10% of the visibility timeout
    delta_seconds = int(visibility_timeout * 0.1)
    elapsed_time = get_localized_now_with_pytz() - start_time
    return elapsed_time.total_seconds() + delta_seconds > visibility_timeout


@app.task(
    name="my-task",
    retry_backoff=5,
    retry_kwargs={'max_retries': 1},
    queue="integrations",
    time_limit=120,  # 2 minutes,
    acks_late=True
)
def my_task(task_id, start_date: datetime.datetime = None):
    logger.info(f"Starting task with id {task_id}")
    if start_date and has_reached_visibility_timeout(start_date):
        logger.info(f"task with id {task_id} reached visibility timeout, exiting")
        return
    time.sleep(40)
    logger.info(f"finished task with id {task_id}")


@app.task(
    name="handler-task",
    retry_backoff=5,
    retry_kwargs={'max_retries': 1},
    queue="integrations",
    time_limit=240,  # 4 minutes,
    acks_late=True
)
def handler(unique_task_id: str, start_date: datetime.datetime, timeout: int = 10):
    now = deepcopy(start_date)
    end = start_date + datetime.timedelta(seconds=timeout)
    task = my_task.delay(task_id=unique_task_id, start_date=start_date)

    while now < end and not task.ready() and not has_reached_visibility_timeout(start_date):
        logger.info(f"waiting for handler to finish, it should finish at {end.isoformat()}")
        time.sleep(5)
        now = get_localized_now_with_pytz()

    if has_reached_visibility_timeout(start_date):
        logger.info(f"visibility timeout reached for handler, finishing")
        return

    while not task.ready():
        logger.info(f"waiting for task with id {unique_task_id} to finish, the end date should be {end.isoformat()}")
        time.sleep(5)

    logger.info(f"finished task with id {unique_task_id}")