from django import forms

from .models import Profile, Link, ClickOnLink, ProfileLevel


class ProfileLevelForm(forms.ModelForm):

    class Meta:
        model = ProfileLevel
        fields = (
            'name',
            'max_num_of_links',
        )
        widgets = {
            'name': forms.TextInput,
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'external_id',
            'profile_level',
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