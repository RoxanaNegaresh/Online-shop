from django import forms
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='username ', max_length=20)
    password = forms.CharField(label='password', max_length=20, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'inputregister'})
        self.fields['password'].widget.attrs.update({'class': 'inputregister'})


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'national_code']
        labels = {
            'username': ' username',
            'password': 'password ',
            'first_name': 'first name',
            'last_name': 'last_name ',
            'national_code': ' national code',

            }
        help_texts = {
            'username': None,  
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'inputregister'})

class OtpForm(forms.Form):
    phone = forms.CharField(label="شماره تماس", max_length=11)
    

class VerifyCode(forms.Form):
    code = forms.CharField(label="کد تایید", max_length=11)

