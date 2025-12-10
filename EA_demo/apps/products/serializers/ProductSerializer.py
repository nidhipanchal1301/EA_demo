from rest_framework import serializers

from apps.products.models import Product, Brand, Category, ProductGroup, ProductVariant, Packaging



class ProductListSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand_name.name',  allow_null=True)
    category_name = serializers.CharField(source='category_name.name',  allow_null=True)
    product_group = serializers.CharField(source='product_group.name',  allow_null=True)
    product_variant = serializers.CharField(source='product_variant.name',  allow_null=True)
    packaging = serializers.CharField(source='packaging.name',  allow_null=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'brand_name', 'category_name', 'product_group','product_variant',\
                'size', 'packaging', 'erp_item_code', )
        read_only_fields = fields


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name', 'product_customer_name', 'brand_name', 'category_name',
            'product_group', 'product_variant', 'packaging', 'size', 'erp_item_code',
            'minimum_order', 'maximum_order', 'notes', 'upload_image', )

    def validate(self, attrs):
        if Product.objects.filter(name=attrs.get('name')).exists():
            raise serializers.ValidationError({'name': 'SKU already exists.'})
        return attrs


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'product_customer_name', 'brand_name', 'category_name', 'product_group', 'product_variant',\
            'size', 'erp_item_code', 'minimum_order', 'maximum_order', 'notes', 'upload_image',)

    def validate(self, attrs):
        product_sku = attrs.get('name') or getattr(self.instance, 'name')
        if Product.objects.filter(name=product_sku).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError({'name': 'Another product with this SKU exists.'})
        return attrs
    

class ProductDetailSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand_name.name', read_only=True)
    category_name = serializers.CharField(source='category_name.name', read_only=True)
    product_group = serializers.CharField(source='product_group_name.name', read_only=True)
    product_variant = serializers.CharField(source='product_variant_name.name', read_only=True)
    packaging = serializers.CharField(source='packaging.name', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_customer_name', 'brand_name', 'category_name', 'product_group',\
            'product_variant', 'packaging', 'size', 'erp_item_code', 'minimum_order', 'maximum_order',\
            'notes', 'upload_image', 'created_at', 'updated_at', )
        read_only_fields = ('id', 'created_at', 'updated_at',)


