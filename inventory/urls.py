# inventory/urls.py
from django.urls import path
from .views import add_item, edit_item

urlpatterns = [
    path('add/', add_item, name='add_item'),
    path('items/', view_items, name='view_items'),
]
