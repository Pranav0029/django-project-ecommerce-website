from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('profile/', views.profile, name='profile'),
    path('re_pass/', views.re_pass, name='re_pass'),

]