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
        max_length=16
    )
    created_at = models.DateTimeField(
        verbose_name='Time of receipt',
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.original_link} from {self.profile}'

    class Meta:
        verbose_name = 'Link'

class ClickOnLink(models.Model):
    link = models.ForeignKey(
        to='ugc.Link',
        verbose_name='Link',
        on_delete=models.CASCADE,
    )
    ip_address = models.TextField(
        verbose_name='IP address'
    )
    click_at = models.DateTimeField(
        verbose_name='Click at that datetime'
    )