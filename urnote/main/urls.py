from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('education/', views.about, name='education')
]
