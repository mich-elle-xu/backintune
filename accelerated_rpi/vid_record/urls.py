from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_video, name='start_video'),
    path('stop/', views.stop_video, name='stop_video'),
]

