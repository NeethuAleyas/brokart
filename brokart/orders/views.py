from django.shortcuts import render,redirect
from .models import Order, Ordered_item
from products.models import Product
from customers.models import Customer
from django.contrib.auth.decorators import login_required
from .models import Order
from django.contrib import messages

def show_cart(request):
    # Assuming the user is authenticated
    user = request.user
    customer=user.customer_profile
    
    # Retrieve the cart items for the current user
    cart_obj,created = Order.objects.get_or_create(owner=user.customer_profile, order_status=Order.CART_STAGE)
    context = {
        'cart': cart_obj
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request):
    if request.POST:
        user = request.user
        try:
            customer = user.customer_profile
        except Customer.DoesNotExist:
            # Handle the case where the Customer profile doesn't exist
            # You might want to create a Customer profile for the user in this case
            customer = Customer.objects.create(user=user, name=user.username, address='', phone='', delete_status=Customer.LIVE)

        quantity = request.POST.get('quantity')
        product_id = request.POST.get('product_id')
        
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        
        product = Product.objects.get(pk=product_id)
        
        ordered_item = Ordered_item.objects.create(
            product=product,
            owner=cart_obj,
            quantity=quantity
        )

    return redirect('cart')

def remove_item_from_cart(request,pk):
    item=Ordered_item.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart')


def checkout_cart(request):
    if request.POST:
        try:
            user = request.user
            customer = user.customer_profile  
            total = float(request.POST.get('total'))

            order_obj = Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )
            if order_obj:
                order_obj.order_status = Order.ORDER_CONFIRMED
                order_obj.total_price = total
                order_obj.save()
                status_message = "Your order is processed. Item will be delivered within 2 days"
                messages.success(request, status_message)
            else:
                status_message = "Unable to process. No items in cart"
                messages.error(request, status_message)
        except Order.DoesNotExist:
            status_message = "Unable to process. No items in cart or Already ordered"
            messages.error(request, status_message)
        except Exception as e:
            status_message = "An error occurred while processing your order."
            messages.error(request, status_message)
    return redirect('cart')


@login_required(login_url='account')
def show_orders(request):
    user=request.user
    customer=user.customer_profile
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders':all_orders}
    return render(request,'my_order.html',context)