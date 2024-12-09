from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'warehouses', views.WarehouseViewSet)
router.register(r'subwarehouses', views.SubWarehouseViewSet)
router.register(r'items', views.InventoryItemViewSet)

urlpatterns = [
    path('api/view_items/', views.view_items, name='view_items'),
    path('api/add_item/', views.add_item, name='add_item'),
    path('api/delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('api/dashboard/stats/', views.get_dashboard_stats, name='dashboard-stats'),
    path('api/', include(router.urls)),
    re_path(r'^.*$', TemplateView.as_view(template_name='frontend/index.html')),  # Serve the React app
]
