from rest_framework import filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from apps.products.models import Product
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView


from apps.products.serializers.ProductSerializer import (
    ProductListSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductDetailSerializer,
)



class ProductListView(ListAPIView):
    queryset = Product.objects.select_related(
        'brand_name', 'category_name', 'product_group', 'product_variant', 'packaging'
    ).distinct()  
    serializer_class = ProductListSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ( 'name', 'brand__name', 'category__name', 'product_group__name',
        'product_variant__name', 'packaging__name', 'erp_item_code', )
    ordering_fields = ('created_at', 'name',)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'pk'


class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer


class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.select_related('brand_name', 'category_name', 'product_group', 'product_variant', 'packaging')
    serializer_class = ProductUpdateSerializer
    lookup_field = 'pk'


