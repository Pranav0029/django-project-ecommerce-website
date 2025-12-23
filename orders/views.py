from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from accounts.models import Customer
from core.models import Cart
from products.models import Product
from .models import Order

def CARD(request):
    customer = Customer.objects.filter(current_user='P').first()

    if not customer:
        return redirect('sign_up')

    # ✅ REMOVE ITEM
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        if cart_id:
            Cart.objects.filter(id=cart_id, customer=customer).delete()
            return redirect('CARD')   # same page reload

    cart_items = Cart.objects.filter(customer=customer).select_related('product')

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'orders/CARD.html', context)

from .models import Order

def order(request, product_id):
    customer = Customer.objects.filter(current_user='P').first()
    if not customer:
        return redirect('sign_up')

    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity',1))#
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        payment_method = request.POST.get('payment_method')

        Order.objects.create(
            customer=customer,
            product=product,
            quantity=quantity,
            price=product.price,
            total_price=product.price * quantity,
            address=address,
            pincode=pincode,
            payment_method=payment_method
        )

        return redirect('order_details')

    context = {
        'customer': customer,
        'product': product
    }
    return render(request, 'orders/order.html', context)


def order_details(request):
    # get current logged customer
    customer = Customer.objects.filter(current_user='P').first()

    # safety check
    if not customer:
        orders = []
    else:
        orders = Order.objects.filter(customer=customer).order_by('-ordered_at')

    return render(request, 'orders/order_details.html', {
        'orders': orders
    })
