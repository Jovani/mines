from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.GameRoomCreate.as_view()),
    path('rooms/open/', views.OpenGameRoom.as_view()),
    path('game/<int:id>/', views.MinesweeperGameRetrieve.as_view()),
]
