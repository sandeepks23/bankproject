from django import forms
from django.contrib.auth.forms import UserCreationForm
from bankapp.models import MyUser
from django.forms import ModelForm
# from bankapp.views import *

class GetUserAccountMixin:
    def get_user_account(self,acc_no):
        try:
            return MyUser.objects.get(account_number=acc_no)
        except:
            return None

class AccountCreationForm(UserCreationForm):
    class Meta:
        model=MyUser
        fields=["first_name","username","email","password1","password2","account_number","account_type","phone","balance"]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class TransactionForm(forms.Form,GetUserAccountMixin):
    from_accountnumber=forms.CharField(max_length=16)
    to_accountnumber=forms.CharField(max_length=16,widget=forms.PasswordInput)
    confirm_accountnumber=forms.CharField(max_length=16)
    amount=forms.FloatField()
    note=forms.CharField(max_length=100)

    def clean(self):
        cleaned_data=super().clean()
        from_accountnumber=cleaned_data.get("from_accountnumber")
        to_accountnumber=cleaned_data.get("to_accountnumber")
        confirm_accountnumber=cleaned_data.get("confirm_accountnumber")
        amount = cleaned_data.get("amount")
        if to_accountnumber!=confirm_accountnumber:
            msg="AccountNumber mismatch"
            self.add_error("confirm_accountnumber",msg)

        user=GetUserAccountMixin()
        account=user.get_user_account(confirm_accountnumber)
        if not account:
            msg="Invalid Account Number"
            self.add_error("confirm_accountnumber",msg)

        account=user.get_user_account(from_accountnumber)

        if account.balance<amount:
            msg="Insufficient Balance"
            self.add_error("amount",msg)






