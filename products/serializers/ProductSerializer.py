from rest_framework import serializers

from products.models import Product, Brand, Category, ProductGroup, ProductVariant, Packaging



class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')
        
class ProductSerializer(serializers.ModelSerializer):
    upload_image = serializers.ImageField(required=False, allow_null=True, use_url=True)
    all_brands = BrandSerializer(source='products', many=True)
    all_categories = serializers.SerializerMethodField()
    all_groups = serializers.SerializerMethodField()
    all_variants = serializers.SerializerMethodField()
    all_packaging = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'product_sku_name',
            'product_customer_name',
            'brand',
            'category',
            'product_group',
            'product_variant',
            'packaging',
            'size',
            'erp_item_code',
            'minimum_order',
            'maximum_order',
            'notes',
            'upload_image',
            'created_at',
            'updated_at',
            # dropdowns
            'all_brands',
            'all_categories',
            'all_groups',
            'all_variants',
            'all_packaging',
        )
        read_only_fields = (
            'id', 'created_at', 'updated_at',
            'all_brands', 'all_categories', 'all_groups', 'all_variants', 'all_packaging'
        )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._all_brands = tuple(Brand.objects.all().values('id', 'name'))
        self._all_categories = tuple(Category.objects.all().values('id', 'name'))
        self._all_groups = tuple(ProductGroup.objects.all().values('id', 'name'))
        self._all_variants = tuple(ProductVariant.objects.all().values('id', 'name', 'product_group'))
        self._all_packaging = tuple(Packaging.objects.all().values('id', 'name'))

    # Return cached dropdowns
    # def get_all_brands(self, obj):
    #     return self._all_brands

    def get_all_categories(self, obj):
        return self._all_categories

    def get_all_groups(self, obj):
        return self._all_groups

    def get_all_variants(self, obj):
        return self._all_variants

    def get_all_packaging(self, obj):
        return self._all_packaging
