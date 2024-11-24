from django.shortcuts import render

from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Order, Client
from .serializers import serializers

# Create your views here.
class ClientList(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = serializers.ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientDetail(APIView):
    def get_client(self, id):
        try:
            return Client.objects.get(id=id)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, id):
        client = self.get_client(id)
        serializer = serializers.ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, id):
        client = self.get_client(id)
        serializer = serializers.ClientUpdateSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, id):
        client = self.get_client(id)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    def get_product(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id):
        product = self.get_product(id)
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = self.get_product(id)
        serializer = serializers.ProductUpdateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, id):
        product = self.get_product(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderList(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    def get_order(self, id):
        try:
            return Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, id):
        order = self.get_order(id)
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, id):
        order = self.get_order(id)
        serializer = serializers.OrderUpdateSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, id):
        order = self.get_order(id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)