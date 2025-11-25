from rest_framework import generics, status
from rest_framework.response import Response

from apps.products.models import BananaGroupStockIn

from apps.products.serializers.BananaGroupStockInSerializer import (
    BananaGroupStockInListSerializer,
    BananaGroupStockInCreateSerializer,
)



class BananaGroupStockInListView(generics.GenericAPIView):
    serializer_class = BananaGroupStockInListSerializer

    def get_queryset(self):
        return BananaGroupStockIn.objects.select_related('product', 'container').all().order_by('-created_at')

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BananaGroupStockInCreateView(generics.GenericAPIView):
    serializer_class = BananaGroupStockInCreateSerializer
    queryset = BananaGroupStockIn.objects.all()

    def post(self, request):
        if request.data.get("action") == "deactivate":
            stock_id = request.data.get("id")
            try:
                obj = self.get_queryset().get(pk=stock_id)
                obj.is_active = False
                obj.save()
                return Response({"message": "Stock deactivated successfully"}, status=200)
            except BananaGroupStockIn.DoesNotExist:
                return Response({"error": "Stock not found"}, status=404)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)






    