from django.urls import path
from . import views
from .views import rhythm_view


urlpatterns = [
    path('', views.find_home, name='find'),
    path('api/rhythm/', rhythm_view),
]
