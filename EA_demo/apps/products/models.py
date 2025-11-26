from django.db import models

from django.core.validators import MinValueValidator



class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class BaseStock(TimeStampedModel):
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    batch_number = models.CharField(max_length=120)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} | {self.batch_number}"



class Brand(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("id",)

    def __str__(self):
        return self.name


class ProductGroup(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Product Group"
        verbose_name_plural = "Product Groups"
        ordering = ("id",)


class ProductVariant(models.Model):
    name = models.CharField(max_length=100)
    product_group_variant = models.ForeignKey(ProductGroup, on_delete=models.CASCADE, related_name="variants")

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        ordering = ("id",)

    def __str__(self):
        return self.name



class Packaging(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Packaging"
        verbose_name_plural = "Packaging Types"
        ordering = ("id",)

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
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("id",)

    def __str__(self):
        return self.name


# FreshStockIn

class FreshStockIn(BaseStock):
    expiry_date = models.DateField(null=True, blank=True)
    inward_qty = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=14, decimal_places=3, null=True, blank=True,  validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = "Fresh Stock-In" 
        verbose_name_plural = "Fresh Stock-In"
        unique_together = ('product', 'batch_number')



#Container

class Container(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Container"
        verbose_name_plural = "Containers"
        ordering = ("id",)

    def __str__(self):
        return self.name


#Banana Group Stock-In

class BananaGroupStockIn(BaseStock):
    container = models.ForeignKey(Container, on_delete=models.PROTECT, related_name='group_stock_ins')
    offload_in_days = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(0)])
    inward_quantity = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(0)])
    min_temperature = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    max_temperature = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    min_humidity = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    max_humidity = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = "Banana Group Stock-In"
        verbose_name_plural = "Banana Group Stock-In"
        unique_together = ('product', 'batch_number')

   