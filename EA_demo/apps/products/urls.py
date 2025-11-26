from django.urls import path

from apps.products.views.ProductViews import *

from apps.products.views.FreshStockInView import (
     FreshStockInListView, 
     FreshStockInCreateView, 
)


from apps.products.views.BananaGroupStockInView import (
    BananaGroupStockInListView,
    BananaGroupStockInCreateView,
)



urlpatterns = [
    # Produts
    path('', ProductListView.as_view(), name='product-list'),
    path('create', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    
     # Fresh Stock-In
    path("fresh-stock", FreshStockInListView.as_view()),
    path("fresh-stock/create", FreshStockInCreateView.as_view()),



    # Banana Group Stock-In
    path("banana-stock", BananaGroupStockInListView.as_view()),
    path("banana-stock/create", BananaGroupStockInCreateView.as_view()),
    
]
