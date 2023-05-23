from datetime import datetime
from rest_framework import permissions, viewsets, filters, views
from rest_framework.response import Response
from .models import Product, OrderProduct, Order
from .serializers import ProductSerializer, OrderSerializer
from .custom_permissions import IsSellerPermission, IsCustomerPermission
from .paginations import MediumRangePagination
from django.http import JsonResponse


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = MediumRangePagination
    permission_classes = []
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsSellerPermission]
        return super().get_permissions()

    search_fields = ['name', 'category__name', 'description', 'price']
    ordering_fields = ['name', 'category__name', 'price']


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated, IsCustomerPermission]
        return super().get_permissions()


class OrderStatisticsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, start_date, end_date, num_products):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Incorrect date format.'}, status=400)

        orders = Order.objects.filter(order_date__gte=start_date, order_date__lte=end_date)
        order_products = OrderProduct.objects.filter(order__in=orders)

        products_dict = {}
        for order_product in order_products:
            if order_product.product.id in products_dict:
                products_dict[order_product.product.id] += order_product.quantity
            else:
                products_dict[order_product.product.id] = order_product.quantity

        sorted_keys = sorted(products_dict, key=products_dict.get, reverse=True)
        top_products = sorted_keys[:num_products]
        result_dict = {key: products_dict[key] for key in top_products}

        return JsonResponse(result_dict)
