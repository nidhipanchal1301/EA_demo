from django.urls import path

from products.views.ProductViews import *



urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('create', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/partial-update', ProductPartialUpdateView.as_view(), name='product-partial-update'),
    path('<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete'),
]
