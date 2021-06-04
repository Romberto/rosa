from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class AuthtificationForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'auth__input'

class RegistrationForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields =('username', 'phone', 'password', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
 
            self.fields[field].widget.attrs['class'] = 'register__input'