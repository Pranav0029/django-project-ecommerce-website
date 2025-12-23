from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.CARD, name='CARD'),

    path('order/<int:product_id>/', views.order, name='order'),

    path("order_details/", views.order_details, name='order_details'),

]