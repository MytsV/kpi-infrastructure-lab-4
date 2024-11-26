from django.urls import path
from . import views

urlpatterns = [
    path('salespersons/', views.SalespersonList.as_view(), name='salesperson_list'),
    path('salespersons/<int:salesperson_id>/', views.SalespersonDetail.as_view(), name='salesperson_detail')
]
