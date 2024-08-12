# accounts/forms.py

from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Politician Name')
    email = forms.IntegerField( required=True, label='Politician Contact Number')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')
    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        

        # if password and confirm_password and password != confirm_password:
        #     self.add_error('confirm_password', "Passwords do not match")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')