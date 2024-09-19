from django.db import models
from accounts.models import User
from product.models import *
# Create your models here.
class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    house_name = models.CharField(max_length=100, null=False)
    street_name = models.CharField(max_length=100, null=False)
    pin_number = models.IntegerField(null=False)
    district = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    country = models.CharField(max_length=50, null=False, default="null")
    phone_number = models.CharField(max_length=50, null=False)
    
    status = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    order_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}, {self.house_name}, {self.street_name}, {self.district}, {self.state}, {self.country}'

    class Meta:
        verbose_name = "User Address"
        verbose_name_plural = "User Addresses"
  

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variant = models.ForeignKey(Product_Variant, on_delete=models.CASCADE)     




class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_at = models.DateField(auto_now_add=True)


    
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type=models.CharField(max_length=500)