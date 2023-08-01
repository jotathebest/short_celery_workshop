import uuid

from tasks import timer


def trigger():
    unique_task_id = str(uuid.uuid4())
    timeout = 80  # seconds
    timer.delay(unique_task_id=unique_task_id, timeout=timeout)


trigger()
