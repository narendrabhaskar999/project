from django.db import models
from django.contrib.auth.models import User

# Model for Customer
class Customer(models.Model):
    ACTIVE=1
    DELETE=0
    DELETE_CHOICES=((ACTIVE,'Live'),(DELETE,'Delete'))
    name=models.CharField(max_length=200)
    address=models.TextField()
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='customer_profile')
    phone=models.CharField(max_length=15)
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=ACTIVE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

