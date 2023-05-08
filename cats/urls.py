from django.urls import path

from .views import cat_list, cat_detail, CatListApi

urlpatterns = [
    path('cats/', CatListApi.as_view()),
    path('cats/<int:pk>/', cat_detail),
]
#path('cats/', cat_list),