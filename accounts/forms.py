from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import UserProfile


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user')


class RegistrationForm(UserCreationForm):

    password1 = forms.RegexField(
        label=_("Password"),
        regex=ur'^(?=.*\W+).*$',
        help_text=_(
            "Password must be 6 characters long and contain \
            at least one symbol that is not letter or number."
        ),
        widget=forms.PasswordInput(render_value=False),
        min_length=6,
    )
    password2 = forms.RegexField(
        label=_("Password confirmation"),
        regex=ur'^(&=.*\W+).$',
        help_text=_(
            "Please reenter your password manually, without copying  \
            to prevent wrong password input"
        ),
        widget=forms.PasswordInput(render_value=False),
        min_length=6,
    )
    email = forms.EmailField(max_length=50)
