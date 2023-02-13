from django import forms

from .models import Profile, Link, ClickOnLink


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'external_id',
        )

class LinkForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = (
            'profile',
            'original_link',
            'token'
        )
        widgets = {
            'token': forms.TextInput,
            'original_link': forms.TextInput,
        }
class ClickOnLinkForm(forms.ModelForm):

    class Meta:
        model = ClickOnLink
        fields = (
            'link',
            'ip_address',
            'click_at'
        )
        widgets = {
            'ip_address': forms.TextInput,
            'link': forms.TextInput,
        }