from django.core.management.base import BaseCommand
from inventory.models import Material, Supplier, PurchaseOrder, MaterialCategory
from django.db.models import Q, F, Sum, Count, OuterRef, Exists


class Command(BaseCommand):
    help = "Run ORM practice queries"

    def handle(self, *args, **options):
        print("\n1️⃣ Suppliers with total stock value:")
        for s in Supplier.objects.prefetch_related('materials').annotate(total=Sum(F('materials__quantity') * F('materials__unit_cost'))):
            print(f"{s.name} → ${s.total:.2f}")

        print("\n2️⃣ Materials low in stock:")
        for m in Material.objects.filter(Q(quantity__lt=F('reorder_level'))):
            print(f"{m.name} → Qty: {m.quantity}")

        criticalStock = Material.objects.filter(Q(quantity__lt=F('reorder_level')) | Q(quantity=0))
        print(f"Critical stock: {list(criticalStock.values('name', 'quantity'))}")

        materialsTotal = Material.objects.aggregate(total=Sum(F('quantity') * F('unit_cost')))
        print(f"Total Material Cost: {materialsTotal['total']}")

        suppliersWithMore3LowStock = Supplier.objects.annotate(low_stock_count=Count('materials', filter=Q(materials__quantity__lt=F('materials__reorder_level')))).filter(low_stock_count__gt=3)
        print(suppliersWithMore3LowStock)

        toolsMaterials = Material.objects.filter(Q(supplier__name__icontains = "Belize") & Q(quantity__gte=F('reorder_level')))
        print(list(toolsMaterials.values("name", "quantity")))

        materials = Material.objects.select_related('supplier', 'category').all()
        for m in materials:
            print(m.category.name)
            print(m.supplier.name)
            print("\n")

        categories = MaterialCategory.objects.filter(materials__supplier__name__icontains = "Belize", materials__quantity__gte=0).distinct().values('name')
        print(categories)

        materials = Material.objects.filter(
            category=OuterRef('pk'),
            supplier__name__icontains='Belize'
        )
        categories = MaterialCategory.objects.annotate(
            has_acme_materials=Exists(materials)
        ).filter(has_acme_materials=True).values('name')
        print(categories)