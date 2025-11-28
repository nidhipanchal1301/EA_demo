from django.db import models

from django.contrib.auth.models import User 

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductGroup(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    name = models.CharField(max_length=100)
    product_group_variant = models.ForeignKey(ProductGroup, on_delete=models.CASCADE, related_name="variants")

    def __str__(self):
        return self.name



class Packaging(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class Product(TimeStampedModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    product_customer_name = models.CharField(max_length=200, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="brand_products", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_products", null=True, blank=True)
    product_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE, related_name="product_group_products", null=True, blank=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="product_variant_products", null=True, blank=True)
    packaging = models.ForeignKey(Packaging, on_delete=models.CASCADE, related_name="packaging_products", null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    erp_item_code = models.CharField(max_length=100, blank=True, null=True)
    minimum_order = models.IntegerField(null=True, blank=True)
    maximum_order = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    upload_image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.name


#Container

class Container(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class OO(models.Model): 
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class StockType(models.Model): 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StockIn(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True)
    batch_number = models.CharField(max_length=120, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='stockins')
    inward_qty = models.IntegerField(null=True, blank=True)
    stock_type = models.ForeignKey(StockType, on_delete=models.PROTECT, null=True, blank=True)
    container = models.ForeignKey(Container, null=True, blank=True,on_delete=models.PROTECT)
    offload_in_days = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    inward_quantity = models.IntegerField(null=True, blank=True)
    min_temperature = models.FloatField(null=True, blank=True)
    max_temperature = models.FloatField(null=True, blank=True)
    min_humidity = models.FloatField(null=True, blank=True)
    max_humidity = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.product.name



   


   