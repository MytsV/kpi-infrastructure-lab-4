from django.urls import path
from . import views

urlpatterns = [
    path('salespersons/', views.SalespersonListCreate.as_view(), name='salesperson_list_create'),
]