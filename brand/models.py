from django.db import models


class Brand(models.Model):
    brand_name= models.CharField( max_length=30)
    brand_image=models.ImageField(upload_to='brand_image/')
    is_active= models.BooleanField(default= True)





    

 