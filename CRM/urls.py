from django.urls import path
from . import views

app_name = "CRM"
urlpatterns = [
    path('', views.index, name='index'),
    
    path('users/', views.detail, name='detail'),
    path('users/<str:username>', views.detail, name='detail'),
    
    path('customer/<str:username>/post/', views.post_customer, name='post_customer'),
    path('customer/<int:customer_id>/put/', views.put_customer, name='put_customer'),
    path('customer/<int:customer_id>/get/', views.get_customer, name='get_customer'),
    
    path('client/post/', views.post_client, name='post_client'),
    path('client/<int:client_id>/get/', views.get_client, name='get_client'),
    
    path('invoice/post/', views.post_invoice, name='post_invoice'),
    path('invoice/<str:invoice_no>/get/', views.get_invoice, name='get_invoice'),
]