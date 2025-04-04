from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.index,name='home'),
    path('product_list/',views.list_products,name='list_product'),
    path('product_detail/<pk>',views.detail_product,name='detail_product'),
    path('',views.index,name='home')
]

