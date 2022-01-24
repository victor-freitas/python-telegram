from django import forms
from .models import Accounts, TelegramApp

class AccountsForm(forms.ModelForm):
     class Meta:
         model = Accounts
         fields = ['name', 'phone', 'api']

class TelegramForm(forms.ModelForm):
    class Meta:
        model = TelegramApp
        fields = ['name', 'api_id', 'api_hash']

class TelegramCodeForm(forms.Form):
        code = forms.CharField(max_length=5,label = 'Código', required = True)
    


   