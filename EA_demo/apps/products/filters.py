import django_filters
from apps.products.models import Product


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class ProductFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name="id", lookup_expr="exact")
    ids = NumberInFilter(field_name="id", lookup_expr="in")

    brand = django_filters.NumberFilter(field_name="brand_name__id", lookup_expr="exact")
    category = django_filters.NumberFilter(field_name="category_name__id", lookup_expr="exact")
    group = django_filters.NumberFilter(field_name="product_group__id", lookup_expr="exact")
    variant = django_filters.NumberFilter(field_name="product_variant__id", lookup_expr="exact")
    packaging = django_filters.NumberFilter(field_name="packaging__id", lookup_expr="exact")

    class Meta:
        model = Product
        fields = ("id", "ids", "brand", "category", "group", "variant", "packaging",)


