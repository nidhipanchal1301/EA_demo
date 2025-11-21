from rest_framework import generics, status
from rest_framework.response import Response

from apps.products.models import BananaGroupStockIn

from apps.products.serializers.BananaGroupStockInSerializer import (
    BananaGroupStockInListSerializer,
    BananaGroupStockInCreateSerializer,
    BananaGroupStockInDeactivateSerializer,
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

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BananaGroupStockInDeactivateView(generics.GenericAPIView):
    serializer_class = BananaGroupStockInDeactivateSerializer
    queryset = BananaGroupStockIn.objects.all()

    def post(self, request, pk, *args, **kwargs):
        try:
            obj = self.get_queryset().get(pk=pk)
            obj.is_active = False
            obj.save()
            return Response({"message": "Stock deactivated successfully"}, status=200)
        except BananaGroupStockIn.DoesNotExist:
            return Response({"error": "Not found"}, status=404)


    