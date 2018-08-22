from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index ),

    # Further allow React Router to take over any URLs not registered with Django
    re_path(r'^.*/', views.index ),
]