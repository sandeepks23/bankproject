from django.urls import path
from django.views.generic import TemplateView
from bankapp.views import AccountCreateView,AccountLoginView,BalanceEnquiryView,FundTransferView,SignOutView,PaymentHistoryView,TransactionFilterView
from django.contrib.auth.decorators import login_required
urlpatterns=[
    path("login",AccountLoginView.as_view(),name="signin"),
    path("register",AccountCreateView.as_view(),name="register"),
    path("home",login_required(TemplateView.as_view(template_name="homepage.html"),login_url="signin"),name="home"),
    path("balance",BalanceEnquiryView.as_view(),name="balance"),
    path("fundtransfer",FundTransferView.as_view(),name="fundtransfer"),
    path("logout",SignOutView.as_view(),name="signout"),
    path("history",PaymentHistoryView.as_view(),name="history"),
    path("filter",TransactionFilterView.as_view(),name="filter")
]