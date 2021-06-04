from django import forms
from clubbisenes.models import Sounds


class SoundForms(forms.ModelForm):
    class Meta:
        model = Sounds
        fields = ('name', 'file', 'description')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'sound__label sound__name'}),
            'file': forms.FileInput(attrs={'class': 'sound__file'}),
            'description': forms.Textarea()
        }


class ModerationForm(forms.Form):
    CHOICES = [('Y', 'Yes'), ('N', 'No')]

    mod = forms.CharField(label='mod', widget=forms.RadioSelect(choices=CHOICES))


class PlayForm(forms.Form):
    play = forms.CharField()


class PayForm(forms.Form):
    pay = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden', 'class': 'popup__input'}))


class AuthForm(forms.Form):
    CHOICES = [('K', 'kassa'), ('D', 'dj')]
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'sound__label sound__name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'sound__label'}))
    role = forms.ChoiceField(choices=CHOICES)


