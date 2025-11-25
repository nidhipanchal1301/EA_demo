from rest_framework import serializers

from apps.products.models import BananaGroupStockIn, Product, Container



class BananaGroupStockInListSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    container = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BananaGroupStockIn
        fields = (
            'id', 'product', 'container', 'batch_number', 'offload_in_days',
            'quantity', 'inward_quantity', 'min_temperature', 'max_temperature',
            'min_humidity', 'max_humidity', 'created_at', )
        read_only_fields = ('id', 'created_at')


class BananaGroupStockInCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    container = serializers.PrimaryKeyRelatedField(queryset=Container.objects.all())

    class Meta:
        model = BananaGroupStockIn
        fields = (
            'product', 'container', 'batch_number', 'offload_in_days',
            'quantity', 'inward_quantity', 'min_temperature', 'max_temperature',
            'min_humidity', 'max_humidity')

    def validate(self, attrs):
        if attrs.get("quantity", 0) < 0:
            raise serializers.ValidationError({"quantity": "Must be non-negative."})

        if attrs.get("inward_quantity", 0) < 0:
            raise serializers.ValidationError({"inward_quantity": "Must be non-negative."})

        return attrs


