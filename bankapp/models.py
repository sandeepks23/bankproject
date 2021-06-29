from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    account_number=models.CharField(max_length=16,unique=True)
    options=(("savings","savings"),
             ("current","current"),
             ("credit","credit"))
    account_type=models.CharField(max_length=20,choices=options,default="savings")
    balance=models.FloatField(max_length=100)
    phone=models.CharField(max_length=12)


class Transactions(models.Model):
    from_accountnumber=models.CharField(max_length=16)
    to_accountnumber=models.CharField(max_length=16)
    amount=models.FloatField()
    note=models.CharField(max_length=100)
    date=models.DateField(auto_now=True)

    