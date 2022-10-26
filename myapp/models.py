from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Product(models.Model):
    def __str__(self):
        return self.Name
    
    def get_absolute_url(self):
        return reverse('myapp:products')


    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    seller_name = models.ForeignKey(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    Brand = models.CharField(max_length=255)
    Description = models.CharField(max_length=2080)
    Stock = models.IntegerField()
    SupplierPrice = models.FloatField()
    SRP = models.FloatField()
    image = models.ImageField(blank=True, upload_to='images')

#Payment Gateway
class OrderDetail(models.Model):
    customer_username = models.CharField(max_length=200)
    product = models.ForeignKey(to='Product',on_delete=models.PROTECT)
    amount = models.IntegerField()
    stripe_payment = models.CharField(max_length=200)
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)




