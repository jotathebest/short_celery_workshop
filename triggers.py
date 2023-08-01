import uuid

from tasks import timer


def trigger():
    task_id = str(uuid.uuid4())
    timeout = 10  # seconds
    timer.delay(task_id=task_id, timeout=timeout)


trigger()
