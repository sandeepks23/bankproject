from django.shortcuts import render,redirect
from django.urls import reverse_lazy

from bankapp.forms import AccountCreationForm,LoginForm,TransactionForm,GetUserAccountMixin
# Create your views here.
from django.views.generic import CreateView,TemplateView
from bankapp.models import MyUser,Transactions
from django.contrib.auth import authenticate,login,logout
from .decorators import loginrequired
from django.utils.decorators import method_decorator
from .filters import TransactionFilter
from django.db.models import Q


class AccountCreateView(CreateView):
    model = MyUser
    form_class = AccountCreationForm
    template_name = "accountcreation.html"
    success_url = reverse_lazy("signin")


class AccountLoginView(TemplateView):
    model=MyUser
    form_class=LoginForm
    template_name = "loginpage.html"
    context={}
    def get(self, request, *args, **kwargs):
        form=self.form_class
        self.context["form"]=form
        return render(request,self.template_name,self.context)

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect("home")
            else:
                print("invalid")
                return redirect("signin")

class SignOutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("signin")

@method_decorator(loginrequired,name="dispatch")

class BalanceEnquiryView(TemplateView):
    model=MyUser
    template_name = "homepage.html"
    context={}
    def get(self, request, *args, **kwargs):
        balance=request.user.balance
        # print(balance)
        self.context["balance"]=balance
        return render(request,self.template_name,self.context)

# class GetUserAccountMixin:
#     def get_user_account(self,acc_no):
#         try:
#             return MyUser.objects.get(account_number=acc_no)
#         except:
#             return None

@method_decorator(loginrequired,name="dispatch")
class FundTransferView(TemplateView,GetUserAccountMixin):
    model=Transactions
    form_class=TransactionForm
    template_name = "fundtransfer.html"
    context={}
    def get(self, request, *args, **kwargs):

        form=self.form_class(initial={"from_accountnumber":request.user.account_number})
        self.context["form"]=form
        return render(request,self.template_name,self.context)

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            from_accountnumber=request.user.account_number
            to_accountnumber=form.cleaned_data.get("confirm_accountnumber")
            # confirm_accountnumber=form.cleaned_data.get("confirm_accountnumber")
            amount=form.cleaned_data.get("amount")
            note=form.cleaned_data.get("note")
            transaction=Transactions(from_accountnumber=from_accountnumber,to_accountnumber=to_accountnumber,amount=amount,note=note)
            transaction.save()
            user=self.get_user_account(from_accountnumber)
            user.balance-=amount
            user.save()
            user=self.get_user_account(to_accountnumber)
            user.balance+=amount
            user.save()
            return redirect("home")
        else:
            form=self.form_class(request.POST)
            self.context["form"]=form
            return render(request,self.template_name,self.context)


@method_decorator(loginrequired,name="dispatch")
class PaymentHistoryView(TemplateView):
    model=Transactions
    template_name = "paymenthistory.html"
    context={}
    def get(self, request, *args, **kwargs):
        ctransactions=self.model.objects.filter(to_accountnumber=request.user.account_number)
        dtransactions=self.model.objects.filter(from_accountnumber=request.user.account_number)
        self.context["ctransactions"]=ctransactions
        self.context["dtransactions"]=dtransactions
        return render(request,self.template_name,self.context)



class TransactionFilterView(TemplateView):
    def get(self, request, *args, **kwargs):
        transactions=Transactions.objects.filter(Q(to_accountnumber=request.user.account_number)|Q(from_accountnumber=request.user.account_number))
        transaction_filter=TransactionFilter(request.GET,queryset=transactions)
        return render(request,"filterhistory.html",{'filter':transaction_filter})




