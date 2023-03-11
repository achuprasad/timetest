import re

from django import forms
from .models import Person

class PersonCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Person
        fields = ('name', 'email', 'role', 'country', 'nationality', 'mobile', 'password1', 'password2')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'role': 'Role',
            'country': 'Country',
            'nationality': 'Nationality',
            'mobile': 'Mobile',
        }
        error_messages = {
            'name': {'required': 'Please enter your name'},
            'email': {'required': 'Please enter your email', 'unique': 'This email is already registered'},
            'role': {'required': 'Please select a role'},
            'country': {'required': 'Please enter your country'},
            'nationality': {'required': 'Please enter your nationality'},
            'mobile': {'required': 'Please enter your mobile number'},
            'password1': {'required': 'Please enter a password'},
            'password2': {'required': 'Please confirm your password'},
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            person = Person.objects.get(email=email)
            raise forms.ValidationError(self.fields['email'].error_messages['unique'], code='unique')
        except Person.DoesNotExist:
            pass

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        if len(password1) < 8 or re.search('[0-9]', password1) is None or re.search('[A-Z]', password1) is None or re.search('[a-z]', password1) is None:
            raise forms.ValidationError("A password should contain at least 8 characters  and a combination of uppercase, lowercase, and numeric characters.")
        return password2


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Person.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is not registered.')
        return email