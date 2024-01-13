from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.create_Room, name='create-room'),
    path('update-room/<str:pk>/', views.update_Room, name='update-room'),
    path('delete-room/<str:pk>/', views.delete_Room, name='delete-room'),
    path('delete-message/<str:pk>/', views.delete_Message, name='delete-message'),
]
