from django.db import models

from accounts.models import *
from product.models import *


# Create your models here.

class OrderAddress(models.Model):
    name = models.CharField(max_length=50, null=False)
    house_name = models.CharField(max_length=500, null=False)
    street_name = models.CharField(max_length=500, null=False)
    pin_number = models.IntegerField(null=False)
    district = models.CharField(max_length=300, null=False)
    state = models.CharField(max_length=300, null=False)
    country = models.CharField(max_length=50, null=False, default="null")
    phone_number = models.CharField(max_length=50, null=False)


class OrderMain(models.Model):
    user = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(OrderAddress, on_delete=models.SET_NULL, null=True)
    total_amount = models.FloatField(null=False)
    date = models.DateField(auto_now_add=True)
    order_status = models.CharField( max_length=100, default="Order Placed")
    payment_option = models.CharField(max_length=100, default="Cash_on_delivery")
    order_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=50)
    
    updated_at = models.DateTimeField(auto_now=True)  
    



class OrderSub(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_order = models.ForeignKey(OrderMain, on_delete=models.CASCADE)
    variant = models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    price = models.FloatField(null=False, default=0)
    quantity = models.IntegerField(null=False, default=0)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=10, null=True,blank=True)
    
    def total_cost(self):
       return self.quantity * self.price

    
   
