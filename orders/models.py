from django.db import models
from customers.models import Customer
from products.models import Product
# Create your models here.
class Order(models.Model):
     # Order status choices
    CART_STAGE = 0
    ORDER_CONFIRMED = 1
    ORDER_PROCESSED = 2
    ORDER_DELIVERED = 3
    ORDER_REJECTED = 4

    STATUS_CHOICE = (
        (CART_STAGE, 'CART_STAGE'),
        (ORDER_CONFIRMED, 'ORDER_CONFIRMED'),
        (ORDER_PROCESSED, 'ORDER_PROCESSED'),
        (ORDER_DELIVERED, 'ORDER_DELIVERED'),
        (ORDER_REJECTED, 'ORDER_REJECTED')
    )

    # Delete status choices
    ACTIVE=1
    DELETE=0
    DELETE_CHOICES=((ACTIVE,'Live'),(DELETE,'Delete'))

    order_status=models.IntegerField(choices=STATUS_CHOICE,default=CART_STAGE)
    owner=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,related_name='orders')
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=ACTIVE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class OrderedItem(models.Model):
    product=models.ForeignKey(Product,related_name='added_carts',on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=1)
    owner=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='added_items')
