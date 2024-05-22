from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Define a simple home view
]
