from rest_framework import status

from rest_framework.generics import ListAPIView, CreateAPIView


from rest_framework.response import Response

from apps.products.models import StockIn

from apps.products.serializers.StockInSerializer import StockInListSerializer, StockInCreateSerializer



class StockInListView(ListAPIView):
    serializer_class = StockInListSerializer

    def get_queryset(self):
        queryset = StockIn.objects.select_related('product', 'created_by').all()
        stock_type = self.request.query_params.get('stock_type')
        created_by_user_id = self.request.query_params.get('created_by')

        if stock_type:
            queryset = queryset.filter(stock_type_id=stock_type)
        if created_by_user_id:
            queryset = queryset.filter(created_by_id=created_by_user_id)

        return queryset



class StockInCreateView(CreateAPIView):
    serializer_class = StockInCreateSerializer
    queryset = StockIn.objects.all()

    def post(self, request, *args, **kwargs):
        rows = request.data.get("rows", [])
        responses = []

        for row in rows:
            if "delete" in row:
                continue
            if "create" in row:
                data = row["create"]
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                product = serializer.validated_data('product')
                batch = serializer.validated_data.get('batch_number')
                stock_type = serializer.validated_data.get('stock_type')
                container = serializer.validated_data.get('container')
                exists = StockIn.objects.filter(product=product, batch_number=batch, stock_type=stock_type, container=container).exists()
                if exists:
                    responses.append({
                        "action": "duplicate",
                        "message": "Duplicate StockIn entry found.",
                        "sku": product.name
                    })
                    continue
                stock_in = StockIn.objects.create(**serializer.validated_data)
                responses.append({"action": "created", "data": StockInListSerializer(stock_in).data})
        return Response(responses, status=status.HTTP_200_OK)

