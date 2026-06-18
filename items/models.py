from django.db import models

# Create your models here.

class Dealer(models.Model):
    dealer_name=models.CharField(max_length=72)
    dealer_phNo=models.IntegerField(max_length=12, null=True, blank=True)
    dealer_add=models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f"{self.dealer_name}"
    
class Item(models.Model):
    date_arrived=models.DateField(null=True, blank=True)
    product_name=models.CharField(max_length=50, null=True, blank=True)
    price=models.FloatField(default=0.00)
    quantity=models.IntegerField(default=0)
    expiry_date=models.DateField(null=True, blank=True)
    dealer=models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.product_name}"
    
class profit(models.Model):
    name=models.CharField(max_length=50, null=True, blank=True)
    total=models.IntegerField()

    def __str__(self):
        return f"{self.name}"
    
class Members(models.Model):
    username=models.CharField(max_length=50)
    password=models.IntegerField()
    def __str__(self):
        return f"{self.username}"


    
