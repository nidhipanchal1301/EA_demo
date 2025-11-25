from rest_framework import serializers

from apps.products.models import FreshStockIn, Product



class FreshStockInListSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FreshStockIn
        fields = ('id', 'product', 'batch_number', 'expiry_date', 'inward_qty', 'total', 'created_at', )
        read_only_fields = ('id', 'created_at', )


class FreshStockInCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = FreshStockIn
        fields = ('product', 'batch_number', 'expiry_date', 'inward_qty', 'total', )
    def validate(self, attrs):

        if attrs.get('inward_qty', 0) < 0:
            raise serializers.ValidationError({'inward_qty': 'Must be non-negative.'})
        if attrs.get('total', 0) < 0:
            raise serializers.ValidationError({'total': 'Must be non-negative.'})
        return attrs


