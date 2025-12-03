from rest_framework import filters, status

from apps.products.models import Product

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView

from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.products.filters import ProductFilter

from apps.products.serializers.ProductSerializer import (
    ProductListSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductDetailSerializer
)



class ProductListView(ListAPIView):
    queryset = Product.objects.select_related(
        'brand_name', 'category_name', 'product_group', 'product_variant', 'packaging'
    ).distinct()  
    serializer_class = ProductListSerializer
    filter_backends = (DjangoFilterBackend,filters.SearchFilter, )
    filterset_class = ProductFilter
    search_fields = ('name', 'brand_name__name', 'category_name__name', 'product_group__name',
        'product_variant__name', 'packaging__name', 'erp_item_code', )
    ordering_fields = ('created_at', 'name',)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'pk'


class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()        
        return Response(ProductListSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.select_related('brand_name', 'category_name', 'product_group', 'product_variant', 'packaging')
    serializer_class = ProductUpdateSerializer
    lookup_field = 'pk'


