from rest_framework import generics, status
from rest_framework.response import Response

from apps.products.models import BananaGroupStockIn

from apps.products.serializers.BananaGroupStockInSerializer import (
    BananaGroupStockInListSerializer,
    BananaGroupStockInCreateSerializer,
    BananaGroupStockInDeleteSerializer,
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



class BananaGroupStockInDeleteView(generics.GenericAPIView):
    serializer_class = BananaGroupStockInDeleteSerializer
    lookup_field = "pk"
    queryset = BananaGroupStockIn.objects.all()

    def delete(self, request, pk):
        obj = self.get_object()
        obj.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
