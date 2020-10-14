from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'validate', 'required': True}))
    first_name = forms.CharField(
        max_length=40, widget=forms.TextInput(attrs={'class': 'validate', 'required': True}))
    last_name = forms.CharField(
        max_length=40, widget=forms.TextInput(attrs={'class': 'validate', 'required': True}))
    username = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={'class': 'validate', 'required': True}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'validate', 'required': True}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'validate', 'required': True}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        self.fields['email'].help_text = "Required."
        self.fields['first_name'].help_text = "Required."
        self.fields['last_name'].help_text = "Required."
        self.fields['password1'].help_text = mark_safe(
            '<ol style="padding-inline-start: 15px;"> <li >Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ol>')
        self.fields['password2'].help_text = "Password confirmation"

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=commit)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        if commit:
            user.save()
        return user
