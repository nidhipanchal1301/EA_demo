from rest_framework import generics, status

from rest_framework.response import Response

from apps.products.models import StockIn

from apps.products.serializers.StockInSerializer import StockInListSerializer, StockInCreateSerializer



class StockInListView(generics.ListAPIView):
    serializer_class = StockInListSerializer

    def get_queryset(self):
        queryset = StockIn.objects.select_related('product', 'stock_type', 'created_by').all().order_by('-created_at')
        stock_type_id = self.request.query_params.get('stock_type')
        oo_id = self.request.query_params.get('oo')

        if stock_type_id:
            queryset = queryset.filter(stock_type_id=stock_type_id)
        if oo_id:
            queryset = queryset.filter(created_by_id=oo_id)

        return queryset



class StockInCreateView(generics.CreateAPIView):
    serializer_class = StockInCreateSerializer
    queryset = StockIn.objects.all()

    def post(self, request, *args, **kwargs):
        rows = request.data.get("rows", [])
        responses = []

        for row in rows:
            if "delete" in row:
                delete_id = row["delete"]
                try:
                    StockIn.objects.get(id=delete_id).delete()
                    responses.append({"action": "deleted", "id": delete_id})
                except StockIn.DoesNotExist:
                    responses.append({"action": "delete_failed", "id": delete_id})
                continue
            if "create" in row:
                serializer = self.serializer_class(data=row["create"])
                serializer.is_valid(raise_exception=True)
                serializer.save()
                responses.append({"action": "created", "data": serializer.data})
        return Response(responses, status=status.HTTP_200_OK)

