from django.db import models
from django.core.exceptions import ValidationError



class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    name = models.CharField(max_length=100)
    product_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE, related_name="variants")

    def __str__(self):
        return f"{self.product_group.name} - {self.name}"


class Packaging(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    


class Product(models.Model):
    product_sku_name = models.CharField(max_length=200)
    product_customer_name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    product_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE, related_name="products")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="products")
    packaging = models.ForeignKey(Packaging, on_delete=models.CASCADE, related_name="products")
    size = models.CharField(max_length=100)
    erp_item_code = models.CharField(max_length=100, blank=True, null=True)
    minimum_order = models.IntegerField()
    maximum_order = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    upload_image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_sku_name



# FreshStockIn

class FreshStockIn(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='fresh_stock_ins')
    batch_number = models.CharField(max_length=120)
    expiry_date = models.DateField(null=True, blank=True)
    inward_qty = models.DecimalField(max_digits=12, decimal_places=3, help_text='Inward quantity (kgs)')
    total = models.DecimalField(max_digits=14, decimal_places=3, help_text='Total (kgs)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['product', 'batch_number'], name='unique_product_batch_fresh')
        ]

    def __str__(self):
        return f"{self.product.product_sku_name} | {self.batch_number}"

    def clean(self):
        if self.inward_qty is not None and self.inward_qty < 0:
            raise ValidationError({'inward_qty': 'Inward quantity must be non-negative.'})
        if self.total is not None and self.total < 0:
            raise ValidationError({'total': 'Total must be non-negative.'})


#Container

class Container(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


#Banana Group Stock-In

class BananaGroupStockIn(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='group_stock_ins')
    container = models.ForeignKey(Container, on_delete=models.PROTECT, related_name='group_stock_ins')
    batch_number = models.CharField(max_length=120)
    offload_in_days = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, help_text='Quantity (units or kgs)')
    inward_quantity = models.DecimalField(max_digits=12, decimal_places=3, help_text='Inward quantity (kgs)')
    min_temperature = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    max_temperature = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    min_humidity = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    max_humidity = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['product', 'batch_number'], name='unique_product_batch_group')
        ]

    def __str__(self):
        return f"{self.product.product_sku_name} | {self.batch_number} | {self.container.name}"

    def clean(self):
        for field in ('quantity', 'inward_quantity', 'min_temperature', 'max_temperature', 'min_humidity', 'max_humidity'):
            val = getattr(self, field, None)
            if val is not None and val < 0:
                raise ValidationError({field: 'Must be non-negative.'})