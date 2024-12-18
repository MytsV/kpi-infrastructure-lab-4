from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.ClientList.as_view(), name='client_list'),
    path('clients/<int:id>/', views.ClientDetail.as_view(), name='client_detail'),
    path('clients/<int:id>/image/<str:size>/', views.ClientImageView.as_view(), name='client_image'),
    path('clients/<int:id>/image/', views.ClientPhotoDeleteView.as_view(), name='client_delete_image'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<int:id>/', views.ProductDetail.as_view(), name='product_detail'),
    path('orders/', views.OrderList.as_view(), name='order_list'),
    path('orders/<int:id>/', views.OrderDetail.as_view(), name='order_detail'),
]
