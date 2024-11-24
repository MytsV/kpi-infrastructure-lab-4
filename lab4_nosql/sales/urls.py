from django.urls import path
from . import views

urlpatterns = [
    path('salespersons/', views.SalespersonList.as_view(), name='salesperson_list'),
    path('salespersons/<str:code>/', views.SalespersonDetail.as_view(), name='salesperson_detail')
]
