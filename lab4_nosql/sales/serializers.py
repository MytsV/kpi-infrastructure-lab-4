from rest_framework import serializers
from .models import Salesperson

class SalespersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salesperson
        fields = ['code', 'full_name', 'age', 'gender', 'phone_number', 'date_joined']