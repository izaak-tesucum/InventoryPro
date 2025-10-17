from rest_framework import serializers
from .models import Material, Supplier, MaterialCategory, PurchaseOrder, StockTransaction


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = ['id', 'name']

class MaterialSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(),
                                                     source='supplier',
                                                     write_only=True
                                                     )
    category_id = serializers.PrimaryKeyRelatedField(queryset=MaterialCategory.objects.all(),
                                                     source='category',
                                                     write_only=True
                                                     )
    total = serializers.SerializerMethodField()

    def validate(self, data):
        if data.get('quantity', 0) < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        if data.get('reorder_level') and data['reorder_level'] < 0:
            raise serializers.ValidationError("Reorder level cannot be negative.")
        return data

    def get_total(self, data):
        return data.total_value

    class Meta:
        model = Material
        fields = ['id', 'name', 'sku', 'quantity', 'reorder_level', 'unit_cost', 'supplier', 'supplier_id', 'category', 'category_id', 'total']

class StockTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransaction
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)
    material_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Material.objects.all(),
        source='materials',
        write_only=True
    )

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'order_number', 'supplier', 'materials', 'material_ids', 'ordered_at', 'received']