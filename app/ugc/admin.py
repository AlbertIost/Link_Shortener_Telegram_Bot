from django.contrib import admin
from .forms import ProfileForm, LinkForm, ClickOnLinkForm
from .models import Profile, Link, ClickOnLink
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id')
    form = ProfileForm

@admin.register(Link)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'original_link', 'token', 'created_at')
    form = LinkForm

@admin.register(ClickOnLink)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'ip_address', 'click_at')
    form = ClickOnLinkForm
