from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product

def home (request):
    if request.method == "POST":
        try:
            product = Product(
                name=request.POST.get('name'),
                category=request.POST.get('category'),
                price=request.POST.get('price'),
                quantity=request.POST.get('quantity'),
                description=request.POST.get('description'),
                image=request.FILES.get('image'),
                image_url=request.POST.get('image_url')
            )

            product.save()
            messages.success(request, "Product added successfully")
            return redirect('add_product')

        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'products/add_product.html')