from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from phonenumbers.phonenumberutil import is_valid_number, parse
from .models import Player


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = Player
        fields = ['new_password1', 'new_password2']


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nickname', 'email', 'phone_number']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        label='Phone Number (optional)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Player
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']


    def clean_username(self):
        username = self.cleaned_data['username']
        username = f"_{username}"
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if phone_number:
            try:
                parsed_number = parse(phone_number, None)

                if not is_valid_number(parsed_number):
                    raise forms.ValidationError("Invalid phone number")
            except Exception:
                raise forms.ValidationError("Invalid phone number")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user

