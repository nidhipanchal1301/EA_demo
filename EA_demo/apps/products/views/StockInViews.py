from rest_framework import status

from rest_framework.generics import ListAPIView, CreateAPIView

from rest_framework.response import Response

from apps.products.models import StockIn

from apps.products.serializers.StockInSerializer import StockInListSerializer, StockInCreateSerializer

from rest_framework.filters import SearchFilter

from django.contrib.auth import get_user_model

User = get_user_model()



class StockInListView(ListAPIView):
    serializer_class = StockInListSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('product__name', 'batch_number', 'container__name', 'stock_type',)

    def get_queryset(self): 
        queryset = StockIn.objects.select_related('product', 'created_by','container',)
        stock_type = self.request.query_params.get('stock_type')
        created_by_user_id = self.request.query_params.get('created_by')
        if stock_type:
            queryset = queryset.filter(stock_type_id=stock_type)
        if created_by_user_id:
            queryset = queryset.filter(created_by_id=created_by_user_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        groups = {}
        for stock in queryset:
            group_key = stock.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if group_key not in groups:
                groups[group_key] = {
                    "id": stock.id, 
                    "stock_in_datetime": stock.created_at.strftime("%d %b %Y %I:%M %p"),
                    "created_by": f"{stock.created_by.username} ({stock.created_by.role})" if stock.created_by else None,
                    "type": stock.stock_type,
                    "items": []
                }
            groups[group_key]["items"].append({
                "product": stock.product.name if stock.product else None,
                "batch_number": stock.batch_number,
                "quantity": stock.quantity,
                "expiry_date": stock.expiry_date.strftime("%d %b %Y") if stock.expiry_date else None
            })
        return Response(list(groups.values()))
    

class StockInCreateView(CreateAPIView):
    serializer_class = StockInCreateSerializer
    queryset = StockIn.objects.all()    

    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({"error": "Expected a list of stock items"}, status=status.HTTP_400_BAD_REQUEST)
        
        items = []
        default_user = User.objects.first()
        for data in request.data:
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                stock_in = serializer.save(created_by=default_user)
                items.append({
                "product": stock_in.product.name,
                "batch_number": stock_in.batch_number,
                "quantity": stock_in.quantity,
                "expiry_date": stock_in.expiry_date.strftime("%d %b %Y") if stock_in.expiry_date else None
            })

        response_data = {
            "id": stock_in.id,
            "stock_in_datetime": stock_in.created_at.strftime("%d %b %Y %I:%M %p"),
            "created_by": f"{default_user.username} ({default_user.role})",
            "type": stock_in.stock_type,
            "items": items
        }

        return Response(response_data, status=status.HTTP_201_CREATED)