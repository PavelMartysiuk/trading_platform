from django.db import models
from django.contrib.auth.models import AbstractUser
from users.enums import OrderType


class User(AbstractUser):
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)


class Currency(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=128, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=128, unique=True)
    logo = models.URLField(max_length=200)
    actual_price = models.IntegerField(blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class WatchList(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('user', 'item')


class Price(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    buy = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sell = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)


class Offer(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    entry_quantity = models.IntegerField()
    quantity = models.IntegerField()
    order_type = models.CharField(max_length=15, choices=OrderType.items())
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_active = models.BooleanField(default=True)


class Inventory(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    reversed_quantity = models.IntegerField()

    class Meta:
        unique_together = ['user', 'item']


class Trade(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                               related_name='seller_trade',
                               related_query_name='seller_trade')
    buyer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                              related_name='buyer_trade',
                              related_query_name='buyer_trade')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    buyer_offer = models.ForeignKey(Offer, null=True, on_delete=models.SET_NULL,
                                    related_name='buyer_trade',
                                    related_query_name='buyer_trade'
                                    )
    seller_offer = models.ForeignKey(Offer, null=True, on_delete=models.SET_NULL,
                                     related_name='seller_trade',
                                     related_query_name='seller_trade'
                                     )
