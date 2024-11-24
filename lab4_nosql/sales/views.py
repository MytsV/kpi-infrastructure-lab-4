from rest_framework import generics
from .models import Salesperson
from .serializers import SalespersonSerializer

class SalespersonListCreate(generics.ListCreateAPIView):
    queryset = Salesperson.objects.all()
    serializer_class = SalespersonSerializer