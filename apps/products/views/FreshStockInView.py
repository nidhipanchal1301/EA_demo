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


class FreshStockInDeactivateView(generics.GenericAPIView):
    serializer_class = FreshStockInListSerializer
    queryset = FreshStockIn.objects.all()

    def post(self, request, pk, *args, **kwargs):
        try:
            stock = self.get_queryset().get(pk=pk)
            if not stock.is_active:
                return Response({"message": "Already deactivated"}, status=status.HTTP_200_OK)
            stock.is_active = False
            stock.save()
            return Response({"message": "Stock deactivated successfully"}, status=status.HTTP_200_OK)
        except FreshStockIn.DoesNotExist:
            return Response({"error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

