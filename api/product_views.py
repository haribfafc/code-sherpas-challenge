from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from .models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'photo_url', 'creator', 'last_modifier']


class CreateProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'photo_url', 'creator', 'last_modifier')

    def create(self, validated_data):
        user = self.context['request'].user
        product = Product.objects.create(
            name=validated_data['name'],
            photo_url=validated_data['photo_url'],
            creator=user,
            last_modifier=user
        )
        return product


class ProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        product = CreateProductSerializer(data=request.data, context={'request': request})
        if product.is_valid():
            product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'photo_url', 'creator', 'last_modifier']

    def update(self, instance, validated_data):
        updated_instance = super().update(instance, validated_data)
        user = self.context['request'].user
        updated_instance.last_modifier = user
        updated_instance.save()
        return updated_instance

class GetUpdateDeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductUpdateSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
