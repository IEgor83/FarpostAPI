from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'custom-error'}),
            'password2': forms.PasswordInput(attrs={'class': 'custom-error'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = '<ul class="custom-error">' + self.fields[
            'password1'].help_text + '</ul>'
        self.fields['password2'].help_text = '<ul class="custom-error">' + self.fields[
            'password2'].help_text + '</ul>'
