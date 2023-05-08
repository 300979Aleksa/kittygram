# from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from .serializers import CatSerializer
from .models import Cat

@api_view(['POST', 'GET'])
def cat_list(request):
    if request.method == 'POST':
        serializer = CatSerializer(data = request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data, status=status.HTTP_201_CREATED)
        return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    cats = Cat.objects.all().order_by('-id')
    serializer = CatSerializer(cats, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def cat_detail(request, pk):
    cat = Cat.objects.get(pk=pk)
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = CatSerializer(instance=cat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = CatSerializer(instance=cat)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class CatListApi(APIView):
    def get(self, request):
        cats = Cat.objects.all().order_by('-id')
        serializer = CatSerializer(cats, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)