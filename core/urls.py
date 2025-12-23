from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.F_page, name='F_page'),
    path('S_page/<int:pk>/', views.S_page, name='S_page'),
    path('J_page', views.J_page, name='J_page'),
    path('search/', views.search, name='search'),
]