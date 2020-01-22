from django import forms
from django.core.validators import EmailValidator


class LoginTokenForm(forms.Form):

    email = forms.CharField(
            label='Мэйл хаяг',
            max_length=250,
            validators=[EmailValidator()],
            error_messages={'required': "оруулна уу!", 'invalid': "Мэйл хаягийг зөв оруулна уу!"},
            widget=forms.EmailInput,
            required=True
        )
