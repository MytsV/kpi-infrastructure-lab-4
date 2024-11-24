from rest_framework import serializers
from .models import Client, Product, Order


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'age', 'gender', 'type', 'price']


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        # Only allow these fields to be updated
        fields = ['name', 'age', 'gender', 'type', 'price']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'type', 'price']


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # Only allow these fields to be updated
        fields = ['type', 'price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['client', 'product']


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # Only allow these fields to be updated
        fields = ['client', 'product']
