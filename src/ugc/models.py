from django.db import models

# Create your models here.
class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='User ID in telegram'
    )

    def __str__(self):
        return f'#{self.external_id}'
    class Meta:
        verbose_name = 'Profile'

class Link(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Profile',
        on_delete=models.CASCADE,
    )
    original_link = models.TextField(
        verbose_name='Original link'
    )
    token = models.TextField(
        verbose_name='Original link token',
        unique=True
    )
    created_at = models.DateTimeField(
        verbose_name='Time of receipt',
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.original_link} from {self.profile}'

    class Meta:
        verbose_name = 'Link'