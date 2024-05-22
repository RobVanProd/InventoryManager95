from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'warehouses', api_views.WarehouseViewSet)
router.register(r'subwarehouses', api_views.SubWarehouseViewSet)
router.register(r'items', api_views.InventoryItemViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('add_item/', views.add_item, name='add_item'),
    path('add_warehouse/', views.add_warehouse, name='add_warehouse'),
    path('add_subwarehouse/', views.add_subwarehouse, name='add_subwarehouse'),
    path('view_items/', views.view_items, name='view_items'),
    path('transfer_item/', views.transfer_item, name='transfer_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('api/', include(router.urls)),
]
