from django.urls import path
from .views import MeViewSet

me_view = MeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('me/', me_view, name='user-me'),
]
