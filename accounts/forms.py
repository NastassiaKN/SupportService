from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Repeat your password'
        })


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

