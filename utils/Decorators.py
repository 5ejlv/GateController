import time
from functools import wraps

def _catch_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {"message": f"Error: {e}"}

    return wrapper