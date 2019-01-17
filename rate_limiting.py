import config
import time

from flask import request, Response

TIMEOUT = 60*60
MAX_LINK = 3 # Number of unique link access + create within timeout
INSERT_LINK_EVENT = "INSERT INTO link_events (ip, link, access_time) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE access_time = %s"
DROP_OLD_LOGS = "DELETE FROM link_events WHERE access_time < %s"
GET_TIMEBOUND_LINK_EVENTS = "SELECT count(*) as count FROM link_events WHERE ip = %s and access_time > %s"

# Will perform rate limit on a request based on caller IP
def rate_limit(func):
    '''
    Sets a rate limit on a given endpoint with `MAX_LINK` links within `TIMEOUT` time
    '''
    def inner_wrapper(*args, **kwargs):
        # Conveniently drop old logs on an access.
        drop_old_logs()

        ip = get_ip()
        access_time = int(time.time())
        bounded_time = access_time - TIMEOUT

        with config.dbconnect() as cursor:
            cursor.execute(GET_TIMEBOUND_LINK_EVENTS, (ip, bounded_time))
            result = cursor.fetchone()

            if result["count"] < MAX_LINK:
                # All good!
                return func(*args, **kwargs)
            else:
                # Rate limit!
                return Response("You're attempting to access too many unique shortened links.", status=429)

    # Flask uses the function name for mapping requests
    # We have to update the wrapper to use the function's name otherwise we cause problems
    inner_wrapper.__name__ = func.__name__
    return inner_wrapper


def drop_old_logs():
    '''
    Drops expired logs (logs older than timeout)
    '''
    with config.dbconnect() as cursor:
        current_time = int(time.time())
        bounded_time = current_time - TIMEOUT
        cursor.execute(DROP_OLD_LOGS, (bounded_time,))


def record_link_event(token):
    '''
    Records a link event or updates an existing link event with a new timestamp
    '''
    with config.dbconnect() as cursor:
        ip = get_ip()
        current_time = int(time.time())
        cursor.execute(INSERT_LINK_EVENT, (ip, token, current_time, current_time))

def get_ip():
    return request.environ['REMOTE_ADDR']
