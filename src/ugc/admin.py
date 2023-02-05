from django.contrib import admin
from .forms import ProfileForm, LinkForm
from .models import Profile
from .models import Link
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm

@admin.register(Link)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'original_link', 'token', 'created_at')
    form = LinkForm
