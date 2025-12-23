from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from accounts.models import Customer
from .models import Cart
from django.db.models import Q
import random


def F_page(request):
    products = Product.objects.all()

    for product in products:
        discount = random.randint(200, 500)
        product.fake_mrp = product.price + discount
        product.offer_amount = discount

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        # 🔥 IMPORTANT FIX — current_user = "P"
        customer = get_object_or_404(Customer, current_user="P")

        cart_item, created = Cart.objects.get_or_create(
            customer=customer,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect("F_page")

    return render(request, "core/F_page.html", {"products": products})


def J_page(request):
    products = Product.objects.filter(category="Expensive Jewellery")

    # --- ADD TO CART LOGIC ---
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        customer = get_object_or_404(Customer, current_user="P")

        cart_item, created = Cart.objects.get_or_create(customer=customer, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect("J_page")
    # -------------------------

    return render(request, 'core/J_page.html', {'products': products})


def S_page(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # --- ADD TO CART LOGIC ---
    if request.method == "POST":
        # In single product page, we use the product from the URL (pk)
        customer = get_object_or_404(Customer, current_user="P")
        cart_item, created = Cart.objects.get_or_create(customer=customer, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect("S_page", pk=pk)
    # -------------------------

    same_category_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:8]
    all_other_products = list(Product.objects.exclude(pk=pk))
    random_products = random.sample(all_other_products, min(len(all_other_products), 4))

    return render(request, 'core/S_page.html', {
        'product': product,
        'same_category_products': same_category_products,
        'random_products': random_products
    })

def search(request):
    query = request.POST.get('search')

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__icontains=query)
    )

    return render(request, 'core/search.html', {
        'products': products,
        'query': query
    })
