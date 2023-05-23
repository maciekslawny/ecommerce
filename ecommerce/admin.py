from django.contrib import admin
from .models import Order, Product, OrderProduct, Category

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Category)