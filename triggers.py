import uuid

from tasks import handler, get_localized_now_with_pytz


def trigger():

    unique_task_id = str(uuid.uuid4())
    timeout = 60  # seconds
    start_date = get_localized_now_with_pytz()
    handler.delay(unique_task_id=unique_task_id, start_date=start_date, timeout=timeout)



trigger()
