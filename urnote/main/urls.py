from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('find/', include('find.urls'), name='find'),
    path('education/', views.about, name='education')
]
