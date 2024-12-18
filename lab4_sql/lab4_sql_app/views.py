from django.shortcuts import render

from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Order, Client
from .serializers import ClientSerializer, ProductSerializer, ProductUpdateSerializer, \
    OrderSerializer, OrderUpdateSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import magic
from rest_framework.parsers import FormParser, MultiPartParser


# Create your views here.
class ClientList(APIView):
    def get(self, request):
        clients = Client.objects.all()

        age_gte = request.query_params.get('age_gte', None)
        if age_gte is not None:
            clients = clients.filter(age__gte=age_gte)

        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
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
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, id):
        client = get_object_or_404(Client, id=id)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, id):
        client = self.get_client(id)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClientImageView(APIView):
    def get(self, request, id, size):
        client = get_object_or_404(Client, id=id)
        if size not in ['small', 'medium', 'large']:
            return Response({'error': 'Invalid image size.'}, status=status.HTTP_400_BAD_REQUEST)

        photo_field = getattr(client, f'photo_{size}', None)
        if photo_field:
            image_data = bytes(photo_field)
            mime = magic.Magic(mime=True)
            content_type = mime.from_buffer(image_data)
            return HttpResponse(image_data, content_type=content_type)
        else:
            return Response({'error': 'Image not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class ClientPhotoDeleteView(APIView):
    def delete(self, request, id):
        client = get_object_or_404(Client, id=id)
        client.delete_images()
        return Response({'message': 'Photos deleted successfully.'}, status=status.HTTP_200_OK)

class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
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
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = self.get_product(id)
        serializer = ProductUpdateSerializer(product, data=request.data)
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

        client_id = request.query_params.get('client_id', None)
        if client_id is not None:
            orders = orders.filter(client_id=client_id)

        product_id = request.query_params.get('product_id', None)
        if product_id is not None:
            orders = orders.filter(product_id=product_id)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
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
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, id):
        order = self.get_order(id)
        serializer = OrderUpdateSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, id):
        order = self.get_order(id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
