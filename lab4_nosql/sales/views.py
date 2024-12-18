from django.http import Http404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Salesperson
from .serializers import SalespersonSerializer, SalespersonUpdateSerializer


class SalespersonList(APIView):
    def get(self, request):
        salespeople = Salesperson.objects.all()

        gender_filter = request.query_params.get('gender', None)
        if gender_filter:
            salespeople = salespeople.filter(gender=gender_filter)

        serializer = SalespersonSerializer(salespeople, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SalespersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SalespersonDetail(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_salesperson(self, salesperson_id):
        try:
            return Salesperson.objects.get(id=salesperson_id)
        except Salesperson.DoesNotExist:
            raise Http404

    def get(self, request, salesperson_id):
        salesperson = self.get_salesperson(salesperson_id)
        serializer = SalespersonSerializer(salesperson)
        return Response(serializer.data)

    def put(self, request, salesperson_id):
        salesperson = self.get_salesperson(salesperson_id)

        serializer = SalespersonUpdateSerializer(salesperson, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, salesperson_id):
        salesperson = self.get_salesperson(salesperson_id)
        salesperson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)