from .models import Link
from django.utils.crypto import get_random_string
def get_new_token() -> str:
    while True:
        token = get_random_string(length=10)
        if not Link.objects.filter(token=token).exists():
            return token
