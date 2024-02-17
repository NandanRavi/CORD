from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRoutes),
    path('rooms/', views.getRooms),
    path('room1/<str:pk>/', views.getRoom),
]
