from django.contrib import admin
from .forms import ProfileForm, LinkForm, ClickOnLinkForm, ProfileLevelForm
from .models import Profile, Link, ClickOnLink, ProfileLevel


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'profile_level')
    form = ProfileForm

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'original_link', 'token', 'created_at')
    form = LinkForm

@admin.register(ClickOnLink)
class ClickOnLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'ip_address', 'click_at')
    form = ClickOnLinkForm


@admin.register(ProfileLevel)
class ProfileLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'max_num_of_links')
    form = ProfileLevelForm
