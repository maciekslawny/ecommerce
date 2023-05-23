from .views import ProductViewSet, OrderViewSet, OrderStatisticsView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('order-statistics/<str:start_date>/<str:end_date>/<int:num_products>/', OrderStatisticsView.as_view(),
         name='order-statistics'),
]
