from .models import Link, Profile
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .utils import get_new_token

class Shortener:
    def __init__(self, user: Profile):
        self.__user = user

    def cut_link(self, url: str) -> Link:
        if url.find('http://') != 0 \
                and url.find('https://') != 0 \
                and url.find('ftp://') != 0 \
                and url.find('ftps://') != 0:

            url = 'https://' + url

        validator = URLValidator()
        try:
            validator(url)
            link, created = Link.objects.get_or_create(
                profile=self.__user,
                original_link=url,
                defaults={
                    'token': get_new_token()
                }
            )
            return link
        except ValidationError as e:
            raise e



    @property
    def user(self):
        return self.__user
