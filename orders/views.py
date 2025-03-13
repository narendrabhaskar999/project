from django.shortcuts import render, redirect
from .models import Order, OrderedItem
from products.models import Product
from django.contrib import messages
from django.http import HttpResponse
from . models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def customer_profile(user):
    # Safely get the customer profile related to the user
    return getattr(user, 'customer_profile', None)

def show_cart(request):
    user = request.user
    customer = customer_profile(user)

    # Check if the customer profile exists
    if not customer:
        messages.error(request, "You need a customer profile to access the cart.")
        return redirect('home')

    # Get or create the cart for the customer
    cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )
    
    context = {'cart': cart_obj}
    return render(request, 'cart.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        customer = customer_profile(user)

        # Check if the customer profile exists
        if not customer:
            messages.error(request, "You need a customer profile to access the cart.")
            return redirect('home')

        quantity = int(request.POST.get('quantity'))  # Ensure this is an integer
        product_id = request.POST.get('product_id')

        # Ensure the product exists
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return redirect('cart')  # Or handle the error properly (e.g., show a message)

        # Get or create the cart for the customer
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        # Check for duplicates in the OrderedItem table
        ordered_item = OrderedItem.objects.filter(
            product=product,
            owner=cart_obj
        ).first()  # Get the first match

        if ordered_item:
            # If the ordered item exists, update its quantity
            ordered_item.quantity += quantity
            ordered_item.save()
        else:
            # If it doesn't exist, create a new ordered item
            ordered_item = OrderedItem.objects.create(
                product=product,
                owner=cart_obj,
                quantity=quantity
            )

        return redirect('cart')

def remove_item_from_cart(request, pk):
    item = OrderedItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart')

def checkout_cart(request):
    try:
        if request.method == 'POST':
            user = request.user
            customer = customer_profile(user)

            # Check if the customer profile exists
            if not customer:
                messages.error(request, "You need a customer profile to access the cart.")
                return redirect('home')

            total = float(request.POST.get('total'))
            order_obj = Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )
            if order_obj:
                order_obj.order_status = Order.ORDER_CONFIRMED
                order_obj.total_price = total
                order_obj.save()
                status_message = "Your order is processed. Your items will be delivered within two days."
                messages.success(request, status_message)
                return redirect('cart')
            else:
                status_message = "Unable to process. No items in the cart."
                messages.error(request, status_message)
                return redirect('cart')
    except Exception as e:
        print("Error:", e)
        return redirect('cart')
    return HttpResponse("Something went wrong")

@login_required(login_url='account')
def show_orders(request):
    user=request.user

    # Check if the user has a customer profile
    try:
        customer=user.customer_profile # Access the related customer_profile
    except Customer.DoesNotExist:
        messages.error(request, "You need a customer profile to access the cart.")
        return redirect('home')
        

    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders':all_orders}

    return render(request, 'orders.html',context)

