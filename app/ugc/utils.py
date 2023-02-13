from django.db.models.functions import Now
from .models import Link, ClickOnLink
from django.utils.crypto import get_random_string


async def get_new_token() -> str:
    while True:
        token = get_random_string(length=10)
        if not await Link.objects.filter(token=token).aexists():
            return token


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def register_click_on_link(link: Link, ip_address: str):
    ClickOnLink.objects.create(
        ip_address=ip_address,
        link=link,
        click_at=Now()
    )
