from django.urls import path

from .views import ImageList, ImageDetail, ImageCreate

urlpatterns = [
    path('', ImageList.as_view(), name='image_list'),
    path('image/<int:pk>/', ImageDetail.as_view(), name='image_detail'),
    path('add_image/', ImageCreate.as_view(), name='image_create'),
]