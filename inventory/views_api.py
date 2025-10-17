from django.db import transaction
from django.db.models import F
from rest_framework import generics, filters
from .models import Material, Supplier
from .permissions import IsInventoryManager
from .serializers import MaterialSerializer, SupplierSerializer, StockTransactionSerializer
from rest_framework import permissions


class MaterialListAPIView(generics.ListAPIView):
    queryset = Material.objects.select_related('supplier', 'category')
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter] # filters.SearchFilter
    # search_fields = ['name','sku','supplier__name', 'category__name']
    ordering_fields = ['quantity','unit_cost', 'name']

    def get_queryset(self):
        qs = Material.objects.select_related('supplier', 'category')
        supplier_id = self.request.query_params.get('supplier', None)
        category = self.request.query_params.get('category', None)
        if supplier_id:
            qs = qs.filter(supplier_id=supplier_id)
        if category:
            qs = qs.filter(category__name__icontains=category)
        return qs

class MaterialCreateAPIView(generics.CreateAPIView):
    queryset = Material.objects.select_related('supplier', 'category')
    serializer_class = MaterialSerializer
    permission_classes = [IsInventoryManager]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SupplierListCreateAPIView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MaterialRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.select_related('supplier', 'category')
    serializer_class = MaterialSerializer
    permission_classes = [IsInventoryManager]

class StockTransactionView(generics.CreateAPIView):
    serializer_class = StockTransactionSerializer
    permission_classes = [IsInventoryManager]

    def perform_create(self, serializer):
        material = serializer.validated_data['material']
        change = serializer.validated_data['change_amount']

        with transaction.atomic():
            material.quantity = F('quantity') + change
            material.save()
            serializer.save(user=self.request.user)