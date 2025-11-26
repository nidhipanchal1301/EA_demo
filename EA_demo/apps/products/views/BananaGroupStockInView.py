from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from apps.products.models import BananaGroupStockIn

from apps.products.serializers.BananaGroupStockInSerializer import (
    BananaGroupStockInListSerializer,
    BananaGroupStockInCreateSerializer,
)



class BananaGroupStockInListView(generics.ListAPIView):
    serializer_class = BananaGroupStockInListSerializer

    def get_queryset(self):
        return BananaGroupStockIn.objects.select_related('product', 'container').all().order_by('-created_at')

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BananaGroupStockInCreateView(generics.CreateAPIView):
    serializer_class = BananaGroupStockInCreateSerializer
    queryset = BananaGroupStockIn.objects.all()

    def post(self, request, *args, **kwargs):
        if request.data.get("action") == "deactivate":
            stock_id = request.data.get("id")
            try:
                obj = self.get_queryset().get(pk=stock_id)
                obj.is_active = False
                obj.save()
                return Response({"message": "Stock deactivated successfully"}, status=200)
            except BananaGroupStockIn.DoesNotExist:
                return Response({"error": "Stock not found"}, status=404)
        return super().post(request, *args, **kwargs)







    