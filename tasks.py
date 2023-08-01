import datetime
import logging
import time
import pytz

from celery import Celery

app = Celery("test-broker")
app.conf.broker_url = "redis://localhost:6379/0"
default_config = 'celeryconfig'
app.config_from_object(default_config)
app.conf.broker_transport_options = {'visibility_timeout': 60}

logger = logging.getLogger(__name__)


def get_localized_now_with_pytz():
    now = datetime.datetime.now(tz=pytz.utc)
    return now


@app.task(
    name="timer-task",
    retry_backoff=5,
    retry_kwargs={'max_retries': 1},
    queue="integrations",
    time_limit=1200,  # 20 minutes,
    acks_late=True
)
def timer(unique_task_id: str, timeout: int = 10):
    logger.info(f"Starting task with id {unique_task_id}")
    now = get_localized_now_with_pytz()
    end = now + datetime.timedelta(seconds=timeout)
    while now < end:
        logger.info(f"waiting for {unique_task_id} to finish, it should finish at {end.isoformat()}")
        time.sleep(5)
        now = get_localized_now_with_pytz()
    logger.info(f"finished task with id {unique_task_id}")
