from rest_framework import serializers

from apps.products.models import StockIn



class StockInListSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name', read_only=True)
    container = serializers.CharField(source='container.name', read_only=True)

    class Meta:
        model = StockIn
        fields = ('id', 'product', 'container', 'stock_type', 'batch_number', 'expiry_date',"created_by", 'quantity', )
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

    def create(self, validated_data):
        obj, created = StockIn.objects.get_or_create(
            product=validated_data['product'],
            batch_number=validated_data.get('batch_number'),
            stock_type=validated_data.get('stock_type'),
            container=validated_data.get('container'),
            defaults=validated_data
        )
        if not created:
            raise serializers.ValidationError("Duplicate entry found.")
        return obj
