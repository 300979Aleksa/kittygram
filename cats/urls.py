from django.urls import path, include

from .views import CatViewSet, OwnerViewSet, LightCatViewSet
from rest_framework.routers import DefaultRouter

# from cats.views import CatList, CatDetail
# from .views import cat_list, cat_detail, CatListApi
# from .views import CatViewSet

router = DefaultRouter()
router.register('cats', CatViewSet)
router.register('owners', OwnerViewSet)
router.register(r'mycats', LightCatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# path('cats/', cat_list),
# path('cats/', CatListApi.as_view()),
# path('cats/<int:pk>/', cat_detail),
# path('cats/', CatList.as_view()),
# path('cats/<int:pk>/', CatDetail.as_view()),