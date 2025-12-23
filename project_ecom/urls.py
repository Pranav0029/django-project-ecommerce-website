from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('accounts/', include('accounts.urls')),

    path('products/', include('products.urls')),

    path('core/', include('core.urls')),

    path('payment/', include('payment.urls')),
    path('orders/', include('orders.urls')),


]

