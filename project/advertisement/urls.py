# urls.py
from django.urls import path
from .views import (
    AdvertisementList, AdvertisementDetail, AdvertisementCreate, AdvertisementUpdate, AdvertisementDelete,
    ResponseCreate, MyResponsesListView, register_user, verify_email, accept_response, delete_response,
    CreateResponseView
)

urlpatterns = [
    path('', AdvertisementList.as_view(), name='advertisement_list'),
    path('<int:pk>/', AdvertisementDetail.as_view(), name='advertisement_detail'),
    path('create/', AdvertisementCreate.as_view(), name='advertisement_create'),
    path('<int:pk>/edit/', AdvertisementUpdate.as_view(), name='advertisement_edit'),
    path('<int:pk>/delete/', AdvertisementDelete.as_view(), name='advertisement_delete'),
    #path('<int:pk>/response/', ResponseCreate.as_view(), name='response_create'),
    path('my-responses/', MyResponsesListView.as_view(), name='my_responses'),
    #path('register/', register_user, name='register_user'),
    path('verify/<str:token>/', verify_email, name='verify_email'),
    path('response/<int:response_id>/accept/', accept_response, name='accept_response'),
    path('response/<int:response_id>/delete/', delete_response, name='delete_response'),
    path('create/<int:advert_id>/', CreateResponseView.as_view(), name='response_create'),
]
