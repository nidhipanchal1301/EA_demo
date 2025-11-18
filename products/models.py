from django.db import models



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
