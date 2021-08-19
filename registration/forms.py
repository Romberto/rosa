from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class AuthtificationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'auth__input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'auth__input'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не найден.')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError(f'Неверный пароль')
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'phone', 'password', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'register__input'
            if field == 'username':
                self.fields[field].widget.attrs["data-validate-field"] = "name"
            elif field == 'phone':
                self.fields[field].widget.attrs["data-validate-field"] = "phone"
            elif field == 'password':
                self.fields[field].widget.attrs["data-validate-field"] = "password1"
            elif field == 'password2':
                self.fields[field].widget.attrs["data-validate-field"] = "password2"

    def clean(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user:
            raise forms.ValidationError(f'Пользовател {username} существует')
        return self.cleaned_data


class FormTableChange(forms.Form):
    numberTable = forms.IntegerField(max_value=50, min_value=1,
                                     widget=forms.NumberInput(attrs={'class': 'input_changeTable'}))
