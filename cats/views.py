from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CatSerializer, OwnerSerializer, CatListSerializer
from .models import Cat, Owner


class CreateRetrieveDeleteViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,viewsets.GenericViewSet):
    # В теле класса никакой код не нужен! Пустячок, а приятно.
    pass

class LightCatViewSet(CreateRetrieveDeleteViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    # def destroy(self, request, *args, **kwargs):
    #    instance = self.get_object()
    #    instance.name = "Пушистик"
    #    instance.save()
    #    serializer = self.get_serializer(instance)
    #    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_path='recent-white-cats')
    def recent_white_cats(self, request):
        # Нужны только последние пять котиков белого цвета
        cats = Cat.objects.filter(color='Белый').order_by('-birth_year')[:5]
        # Передадим queryset cats сериализатору 
        # и разрешим работу со списком объектов
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        # Если запрошенное действие (action) — получение списка объектов ('list')
        if self.action == 'list':
            # ...то применяем CatListSerializer
            return CatListSerializer
        # А если запрошенное действие — не 'list', применяем CatSerializer
        return CatSerializer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer 



# Создаётся роутер
# router = SimpleRouter()
# Вызываем метод .register с нужными параметрами
# router.register('cats', CatViewSet)
# В роутере можно зарегистрировать любое количество пар "URL, viewset":
# например
# router.register('owners', OwnerViewSet)
# Но нам это пока не нужно

# urlpatterns = [
    # Все зарегистрированные в router пути доступны в router.urls
    # Включим их в головной urls.py
#    path('', include(router.urls)),
#]
#
# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import viewsets
# Create your views here.
# from .serializers import CatSerializer
# from .models import Cat
#
# class CatViewSet(viewsets.ModelViewSet):
#    queryset = Cat.objects.all()
#    serializer_class = CatSerializer
#
# @api_view(['POST', 'GET'])
# def cat_list(request):
#    if request.method == 'POST':
#        serializer = CatSerializer(data = request.data, many=True)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(data = serializer.data, status=status.HTTP_201_CREATED)
#        return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#    cats = Cat.objects.all().order_by('-id')
#    serializer = CatSerializer(cats, many=True)
#    return Response(data=serializer.data, status=status.HTTP_200_OK)
#
# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def cat_detail(request, pk):
#    cat = Cat.objects.get(pk=pk)
#    if request.method == 'PUT' or request.method == 'PATCH':
#        serializer = CatSerializer(instance=cat, data=request.data, partial=True)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_200_OK)
#        return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#    elif request.method == 'DELETE':
#        cat.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
#    serializer = CatSerializer(instance=cat)
#    return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#
# class CatListApi(APIView):
#    def get(self, request):
#        cats = Cat.objects.all().order_by('-id')
#        serializer = CatSerializer(cats, many=True)
#        return Response(data=serializer.data, status=status.HTTP_200_OK)
#    
#    def post(self, request):
#        serializer = CatSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED) 
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
# class CatList(generics.ListCreateAPIView):
#    queryset = Cat.objects.all()
#    serializer_class = CatSerializer
#
# class CatDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Cat.objects.all()
#    serializer_class = CatSerializer