from rest_framework import serializers

from apps.products.models import Product, Brand, Category, ProductGroup, ProductVariant, Packaging



class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ('id', 'name')


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ('id', 'name', 'product_group')


class PackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packaging
        fields = ('id', 'name')



class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    product_group = ProductGroupSerializer(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)
    packaging = PackagingSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'product_sku_name', 'product_customer_name', 'brand', 'category', 'product_group',\
            'product_variant', 'packaging', 'size', 'erp_item_code', 'minimum_order', 'maximum_order',\
            'notes', 'upload_image', 'created_at', 'updated_at', )
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'product_sku_name', 'product_customer_name', 'brand', 'category',
            'product_group', 'product_variant', 'packaging', 'size', 'erp_item_code',
            'minimum_order', 'maximum_order', 'notes', 'upload_image', )

    def validate(self, attrs):
        if Product.objects.filter(product_sku_name=attrs.get('product_sku_name')).exists():
            raise serializers.ValidationError({'product_sku_name': 'SKU already exists.'})
        return attrs


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_sku_name', 'product_customer_name', 'brand', 'category', 'product_group', 'product_variant',\
            'packaging', 'size', 'erp_item_code', 'minimum_order', 'maximum_order', 'notes', 'upload_image',)

    def validate(self, attrs):
        product_sku = attrs.get('product_sku_name') or getattr(self.instance, 'product_sku_name')
        if Product.objects.filter(product_sku_name=product_sku).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError({'product_sku_name': 'Another product with this SKU exists.'})
        return attrs

class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    product_group = ProductGroupSerializer(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)
    packaging = PackagingSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'product_sku_name', 'product_customer_name', 'brand', 'category', 'product_group',\
            'product_variant', 'packaging', 'size', 'erp_item_code', 'minimum_order', 'maximum_order',\
            'notes', 'upload_image', 'created_at', 'updated_at', )
        read_only_fields = ('id', 'created_at', 'updated_at')


