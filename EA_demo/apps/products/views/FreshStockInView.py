from rest_framework import generics, status
from rest_framework.response import Response

from apps.products.models import FreshStockIn, Product

from apps.products.serializers.FreshStockInSerializer import FreshStockInCreateSerializer, FreshStockInListSerializer



class FreshStockInListView(generics.ListAPIView):
    serializer_class = FreshStockInListSerializer

    def get_queryset(self):
        return FreshStockIn.objects.select_related('product').all().order_by('-created_at')

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FreshStockInCreateView(generics.CreateAPIView):
    serializer_class = FreshStockInCreateSerializer
    queryset = FreshStockIn.objects.all()

    def post(self, request, *args, **kwargs):
        action = request.data.get("action")
        if action == "deactivate":
            stock_id = request.data.get("id")
            try:
                stock = FreshStockIn.objects.get(id=stock_id)
                stock.is_active = False
                stock.save()
                return Response({"message": "Stock deactivated"}, status=200)
            except FreshStockIn.DoesNotExist:
                return Response({"error": "Not found"}, status=404)
        return super().post(request, *args, **kwargs)
        
  



