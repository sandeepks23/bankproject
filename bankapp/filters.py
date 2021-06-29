import django_filters
from .models import Transactions

class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model=Transactions
        fields=["date","amount","from_accountnumber","to_accountnumber"]