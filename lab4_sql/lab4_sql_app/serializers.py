from rest_framework import serializers
from .models import Client, Product, Order
import base64


class ClientSerializer(serializers.ModelSerializer):

    photo_small_base64 = serializers.SerializerMethodField()
    photo_medium_base64 = serializers.SerializerMethodField()
    photo_large_base64 = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'name', 'age', 'gender', 'type', 'price', 'photo_small_base64', 'photo_medium_base64',
                  'photo_large_base64']
    
    def get_photo_small_base64(self, obj):
        if obj.photo_small:
            return bytes(obj.photo_small).decode('latin1')
        return None
    
    def get_photo_medium_base64(self, obj):
        if obj.photo_medium:
            return bytes(obj.photo_medium).decode('latin1')
        return None

    def get_photo_large_base64(self, obj):
        if obj.photo_large:
            return bytes(obj.photo_large).decode('latin1')
        return None


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        # Only allow these fields to be updated
        fields = ['name', 'age', 'gender', 'type', 'price']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        extra_kwargs = {
            'price': {'min_value': 0.00}
        }
        fields = ['id', 'type', 'price']


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # Only allow these fields to be updated
        extra_kwargs = {
            'price': {'min_value': 0.00}
        }
        fields = ['type', 'price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'client', 'product']

    def to_representation(self, instance):
        self.fields['client'] = ClientSerializer(read_only=True)
        self.fields['product'] = ProductSerializer(read_only=True)
        return super().to_representation(instance)


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # Only allow these fields to be updated
        fields = ['client', 'product']
