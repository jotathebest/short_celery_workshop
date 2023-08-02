# Setup

1. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
2. Install docker by following the instructions for your OS at <https://docs.docker.com/engine/install/>.
3. In one terminal, run the following command to start the Redis docker container:
    ```bash
    docker run -d -it -p 6379:6379 redis:5.0-alpine
3. In another terminal, run the following command to start the Celery worker:
    ```bash
    celery -A tasks worker --loglevel=INFO -c 1
    ```
4. In another terminal, run the following command to trigger the celery task:
    ```bash
      python triggers.py
    ```
