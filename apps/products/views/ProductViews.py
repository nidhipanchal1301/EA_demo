from rest_framework import generics, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from apps.products.models import Product

from apps.products.serializers.ProductSerializer import (
    ProductListSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductDetailSerializer,
)



class ProductListView(generics.ListAPIView):
    queryset = Product.objects.select_related(
        'brand', 'category', 'product_group', 'product_variant', 'packaging'
    ).distinct()  
    serializer_class = ProductListSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ( 'product_sku_name', 'brand__name', 'category__name', 'product_group__name',
        'product_variant__name', 'packaging__name', 'erp_item_code', )
    ordering = ('-created_at',)

    ordering_fields = ('created_at', 'product_sku_name')
    ordering = ('-created_at',)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'pk'


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.select_related('brand', 'category', 'product_group', 'product_variant', 'packaging')
    serializer_class = ProductUpdateSerializer
    lookup_field = 'pk'
    # parser_classes = (MultiPartParser, FormParser, JSONParser)


