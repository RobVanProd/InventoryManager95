# inventory/urls.py
from django.urls import path
from .views import home, add_item, view_items

urlpatterns = [
    path('', home, name='home'),
    path('add/', add_item, name='add_item'),
    path('items/', view_items, name='view_items'),
]
