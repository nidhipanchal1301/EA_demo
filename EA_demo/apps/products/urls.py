from django.urls import path

from apps.products.views.ProductViews import *

from apps.products.views.StockInViews import StockInListView, StockInCreateView



urlpatterns = [
    # Produts
    path('', ProductListView.as_view(), name='product-list'),
    path('create', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    
    path("stock-in/", StockInListView.as_view(), name="stockin-list"),
    path("stock-in/create/", StockInCreateView.as_view(), name="stockin-create"),
    
]
