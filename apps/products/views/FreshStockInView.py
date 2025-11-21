from rest_framework import generics, status
from rest_framework.response import Response
from apps.products.models import FreshStockIn, Product
from apps.products.serializers.FreshStockInSerializer import FreshStockInCreateSerializer, FreshStockInListSerializer



class FreshStockInListView(generics.GenericAPIView):
    serializer_class = FreshStockInListSerializer

    def get_queryset(self):
        return FreshStockIn.objects.select_related('product').all().order_by('-created_at')

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FreshStockInCreateView(generics.GenericAPIView):
    serializer_class = FreshStockInCreateSerializer
    queryset = FreshStockIn.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FreshStockInDeleteView(generics.DestroyAPIView):
    queryset = FreshStockIn.objects.all()

    def delete(self, request, pk, *args, **kwargs):
        try:
            fresh_stock = self.get_object()
            fresh_stock.delete()
            return Response({"message": "Stock deleted successfully"}, status=204)
        except FreshStockIn.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

