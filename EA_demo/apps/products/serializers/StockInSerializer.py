from rest_framework import serializers

from apps.products.models import StockIn



class StockInListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.__str__', read_only=True)
    product = serializers.CharField(source='product.name', read_only=True)
    container = serializers.CharField(source='container.name', read_only=True)

    class Meta:
        model = StockIn
        fields = ('id', 'product', 'container', 'stock_type', 'batch_number', 'expiry_date',"created_by", 'quantity','created_at', )
        read_only_fields = fields


class StockInCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockIn
        fields = (
            'product', 'container', 'stock_type', 'batch_number', 'expiry_date', "created_by",
            'inward_qty', 'quantity', 'inward_quantity', 'offload_in_days',
            'min_temperature', 'max_temperature', 'min_humidity', 'max_humidity', )

    def validate(self, attrs):
        for field in ['inward_qty', 'quantity', 'inward_quantity']:
            if attrs.get(field, 0) < 0:
                raise serializers.ValidationError({field: "Must be non-negative."})
        return attrs
