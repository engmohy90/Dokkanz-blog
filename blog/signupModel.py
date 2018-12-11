from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(u'this email exist')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, validators=[validate_email],
                             help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
