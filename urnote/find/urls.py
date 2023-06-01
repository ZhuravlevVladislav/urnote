from django.urls import path
from . import views

from .views import MillisecondsView

urlpatterns = [
    path('', views.find_home, name='find'),
    path('milliseconds/', MillisecondsView.as_view()),
]
