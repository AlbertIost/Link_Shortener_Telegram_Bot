from django import forms

from .models import Profile, Link


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'external_id',
            'name',
        )
        widgets = {
            'name': forms.TextInput
        }

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