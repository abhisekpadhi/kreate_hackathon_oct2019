from django.db import models
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[6789]\d{9}$',
    message="Phone number must be entered in the format: \"+917760601643\". Up to 13 digits allowed."
)


class User(models.Model):
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    is_collector = models.BooleanField(default=False)
    privkey = models.TextField(default="")
    pubkey = models.TextField(default="")


class Order(models.Model):
    is_paid = models.BooleanField(default=False)
    total = models.BigIntegerField(null=False, default=0)
    user = models.ForeignKey('User', on_delete=models.CASCADE)


class OrderPickup(models.Model):
    collector = models.ForeignKey('User', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_failed = models.BooleanField(default=False)


class Transaction(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    paid_by = models.BigIntegerField(null=True)
    paid_to = models.BigIntegerField(null=True)
    amt = models.BigIntegerField(null=False, default=0)
    is_done = models.BooleanField(default=False)

