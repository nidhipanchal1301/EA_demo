from rest_framework import generics, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from products.models import Product

from products.serializers.ProductSerializer import ProductSerializer



class ProductListView(generics.ListAPIView):
    queryset = Product.objects.select_related(
        'brand', 'category', 'product_group', 'product_variant', 'packaging'
    ).distinct()  

    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)

    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    search_fields = (
        'product_sku_name',
        'brand__name',
        'category__name',
        'product_group__name',
        'product_variant__name',
        'packaging__name',
        'erp_item_code',
    )

    ordering_fields = ('created_at', 'product_sku_name')
    ordering = ('-created_at',)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser )


    def post(self, request, *args, **kwargs):
        print("FILES:", request.FILES)
        print("DATA:", request.data)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    parser_classes = (MultiPartParser, FormParser, JSONParser)


class ProductPartialUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['patch', 'head', 'options']


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
