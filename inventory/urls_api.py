from django.urls import path
from . import views_api

urlpatterns = [
    path('materials/', views_api.MaterialListAPIView.as_view(), name='materials-list'),
    path('materials/create/', views_api.MaterialCreateAPIView.as_view(), name='materials-add'),
    path('materials/<int:pk>/', views_api.MaterialRetrieveUpdateDestroyAPIView.as_view(), name='materials-detail'),
    path('suppliers/', views_api.SupplierListCreateAPIView.as_view(), name='suppliers-list'),
    path('transactions/', views_api.StockTransactionView.as_view(), name='transactions'),
]
