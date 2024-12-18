from rest_framework import serializers
from .models import Client, Product, Order
import base64


class ClientSerializer(serializers.ModelSerializer):
    upload_photo = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Client
        fields = ['id', 'name', 'age', 'gender', 'type', 'price', 'upload_photo']

    def create(self, validated_data):
        upload_photo = validated_data.pop('upload_photo', None)
        client = Client.objects.create(**validated_data)
        if upload_photo:
            client._uploaded_photo = upload_photo
            client.save()
        return client

    def update(self, instance, validated_data):
        upload_photo = validated_data.pop('upload_photo', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if upload_photo:
            instance._uploaded_photo = upload_photo
        instance.save()
        return instance


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        # Only allow these fields to be updated
        fields = ['name', 'age', 'gender', 'type', 'price', 'delete_photos']

    def update(self, instance, validated_data):
        if validated_data.pop('delete_photos', False):
            instance.delete_images()
        return super().update(instance, validated_data)


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
