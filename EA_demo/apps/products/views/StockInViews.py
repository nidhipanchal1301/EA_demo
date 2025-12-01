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
                serializer = self.serializer_class(data=row["create"])
                serializer.is_valid(raise_exception=True)
                serializer.save()
                responses.append({"action": "created", "data": serializer.data})
        return Response(responses, status=status.HTTP_200_OK)

