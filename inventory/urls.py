from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'warehouses', api_views.WarehouseViewSet)
router.register(r'subwarehouses', api_views.SubWarehouseViewSet)
router.register(r'items', api_views.InventoryItemViewSet)

urlpatterns = [
    path('add_item/', views.add_item, name='add_item'),
    path('add_warehouse/', views.add_warehouse, name='add_warehouse'),
    path('add_subwarehouse/', views.add_subwarehouse, name='add_subwarehouse'),
    path('view_items/', views.view_items, name='view_items'),
    path('transfer_item/', views.transfer_item, name='transfer_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('api/', include(router.urls)),
    re_path(r'^.*$', TemplateView.as_view(template_name='frontend/index.html')),  # Serve the React app
]
