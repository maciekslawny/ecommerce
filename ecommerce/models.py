import datetime
from django.db import models
from django.conf import settings
from .scripts.confirmation_email import order_confirmation_email
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=512)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='product_photos', blank=True, null=True)
    image_thumbnail = models.ImageField(upload_to='product_photos', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            max_width = 200
            thumbnail_img = img
            if img.width > max_width:
                ratio = max_width / img.width
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)
                thumbnail_img = thumbnail_img.resize((new_width, new_height), Image.ANTIALIAS)
            thumbnail_path = f'{self.image.path.replace(".", "_thumbnail.")}'
            thumbnail_img.save(thumbnail_path, quality=90)
            self.image_thumbnail.name = thumbnail_path
            super(Product, self).save(*args, **kwargs)


class Order(models.Model):
    ACTIVE = 1
    REQUESTED = 2

    STATUSES = (
        (ACTIVE, 'Active'),
        (REQUESTED, 'Requested'),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    second_name = models.CharField(max_length=32)
    address = models.TextField(max_length=512)
    order_date = models.DateField(default=datetime.date.today)
    status = models.PositiveSmallIntegerField(choices=STATUSES, blank=False, null=False, default=ACTIVE)

    def __str__(self):
        return f'{self.customer} - {self.order_date}'

    @property
    def total_price(self):
        total_price = 0

        order_items = self.order_products.all()

        for order_item in order_items:
            total_price += order_item.total_price

        return total_price

    @property
    def payment_date(self):
        return self.order_date + datetime.timedelta(days=5)

    def save(self, *args, **kwargs):
        if self.pk:
            previous_order = Order.objects.get(pk=self.pk)
            if previous_order.status == self.ACTIVE and self.status == self.REQUESTED:
                Order.objects.filter(customer=self.customer).exclude(pk=self.pk).update(status=self.REQUESTED)
                new_order = Order(customer=self.customer, status=self.ACTIVE)
                new_order.save()
                order_confirmation_email(self)
        super().save(*args, **kwargs)


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def total_price(self):
        return self.product.price * self.quantity
