import random
import string

from yacut.models import URLMap


ALLOWED_SHORT_CHARS = string.ascii_letters + string.digits


def generate_short_id(length: int = 6) -> str:
    return ''.join(random.choice(ALLOWED_SHORT_CHARS) for _ in range(length))


def get_unique_short_id(length: int = 6) -> str:
    # Ensure uniqueness against database and avoid reserved names
    reserved = {'files'}
    while True:
        candidate = generate_short_id(length)
        if candidate in reserved:
            continue
        if not URLMap.query.filter_by(short=candidate).first():
            return candidate