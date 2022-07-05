import os
import redis
from rq import Worker, Queue, Connection
from api.helpers import create_spotify_playlist
from worker import conn

listen = ["high", "default", "low"]

redis_url = os.getenv("REDISTOGO_URL", "redis://localhost:6379")

conn = redis.from_url(redis_url)

if __name__ == "__main__":
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()

q = Queue(connection=conn)


result = q.enqueue(
    create_spotify_playlist, "https://team-tornado-mixtape.herokuapp.com/"
)
