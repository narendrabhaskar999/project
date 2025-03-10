from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.index,name='home'),
    path('product_list/',views.list_products,name='list_product'),
    path('product_detail',views.detail_product,name='detail_product')
]

