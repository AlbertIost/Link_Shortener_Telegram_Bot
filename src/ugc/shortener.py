from .models import Link, Profile
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .utils import get_new_token

class Shortener:
    def __init__(self, user: Profile):
        self.__user = user

    def cut_link(self, url: str) -> Link:
        validator = URLValidator()
        try:
            validator(url)
            link = Link.objects.create(
                profile=self.__user,
                original_link=url,
                token=get_new_token()
            )
            return link
        except ValidationError as e:
            raise e



    @property
    def user(self):
        return self.__user
