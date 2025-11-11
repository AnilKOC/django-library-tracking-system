from contextlib import contextmanager
from functools import wraps

import redis
from django.conf import settings
from redis.exceptions import LockNotOwnedError

redis_client = redis.Redis.from_url(settings.CELERY_BROKER_URL)


@contextmanager
def redis_lock(lock_key: str, expire: int = 60):
    lock = redis_client.lock(lock_key, timeout=expire)
    acquired = lock.acquire(blocking=False)
    try:
        yield acquired
    finally:
        if acquired:
            try:
                lock.release()
            except LockNotOwnedError:
                pass


def task_lock(name: str = None, expire: int = 60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            lock_name = name or f"celery_lock:{func.__name__}"
            with redis_lock(lock_name, expire=expire) as acquired:
                if not acquired:
                    print(f"⚠️ {func.__name__} already running, skipping.")
                    return None
                print(f"✅ {func.__name__} task accuried, running...")
                return func(*args, **kwargs)

        return wrapper

    return decorator
