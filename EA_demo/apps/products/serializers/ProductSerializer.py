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
        fields = ('id', 'name', 'product_group_variant')


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
        fields = ('id', 'name', 'product_customer_name', 'brand', 'category', 'product_group',\
            'product_variant', 'packaging', 'size', 'erp_item_code', 'minimum_order', 'maximum_order',\
            'notes', 'upload_image', 'created_at', 'updated_at', )
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name', 'product_customer_name', 'brand', 'category',
            'product_group', 'product_variant', 'packaging', 'size', 'erp_item_code',
            'minimum_order', 'maximum_order', 'notes', 'upload_image', )

    def validate(self, attrs):
        if Product.objects.filter(name=attrs.get('name')).exists():
            raise serializers.ValidationError({'name': 'SKU already exists.'})
        return attrs


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'product_customer_name', 'brand', 'category', 'product_group', 'product_variant',\
            'packaging', 'size', 'erp_item_code', 'minimum_order', 'maximum_order', 'notes', 'upload_image',)

    def validate(self, attrs):
        product_sku = attrs.get('name') or getattr(self.instance, 'name')
        if Product.objects.filter(name=product_sku).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError({'name': 'Another product with this SKU exists.'})
        return attrs

class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    product_group = ProductGroupSerializer(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)
    packaging = PackagingSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_customer_name', 'brand', 'category', 'product_group',\
            'product_variant', 'packaging', 'size', 'erp_item_code', 'minimum_order', 'maximum_order',\
            'notes', 'upload_image', 'created_at', 'updated_at', )
        read_only_fields = ('id', 'created_at', 'updated_at')


