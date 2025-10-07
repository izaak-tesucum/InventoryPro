from django.db import migrations

def seed_data(apps, schema_editor):
    Supplier = apps.get_model('inventory', 'Supplier')
    Material = apps.get_model('inventory', 'Material')

    # Clear existing records
    Material.objects.all().delete()
    Supplier.objects.all().delete()

    # Suppliers
    suppliers = [
        {"id": 1, "name": "Belize Hardware Supply Co.", "contact_person": "Carlos Mendez", "phone": "+501-223-4567", "email": "c.mendez@bhsupply.com"},
        {"id": 2, "name": "Caribbean Concrete Ltd.", "contact_person": "Angela Castillo", "phone": "+501-225-9876", "email": "acastillo@caribconcrete.com"},
        {"id": 3, "name": "Greenwood Lumber & Timber", "contact_person": "John Alvarez", "phone": "+501-222-3344", "email": "jalvarez@greenwoodtimber.com"},
        {"id": 4, "name": "Central Electrical Distributors", "contact_person": "Maria Hernandez", "phone": "+501-227-1122", "email": "mhernandez@cedbelize.com"},
        {"id": 5, "name": "Belize Paints & Finishes", "contact_person": "Rafael Torres", "phone": "+501-226-7788", "email": "rtorres@belizepaints.com"},
    ]
    Supplier.objects.bulk_create([Supplier(**s) for s in suppliers])

    # Materials
    materials = [
        {"id": 1, "name": "Cement Bag (50kg)", "sku": "CEM-50KG", "category": "Building Materials", "supplier_id": 2, "quantity": 500, "reorder_level": 100, "unit_cost": 9.50},
        {"id": 2, "name": "Rebar Steel Rod (10mm)", "sku": "REB-10MM", "category": "Steel", "supplier_id": 2, "quantity": 1200, "reorder_level": 200, "unit_cost": 6.25},
        {"id": 3, "name": "Plywood Sheet (4x8)", "sku": "PLY-48", "category": "Wood", "supplier_id": 3, "quantity": 300, "reorder_level": 50, "unit_cost": 32.00},
        {"id": 4, "name": "Electrical Wire Roll (100m)", "sku": "WIRE-100", "category": "Electrical", "supplier_id": 4, "quantity": 150, "reorder_level": 30, "unit_cost": 45.75},
        {"id": 5, "name": "Light Switch (Standard)", "sku": "SWI-STD", "category": "Electrical", "supplier_id": 4, "quantity": 400, "reorder_level": 100, "unit_cost": 3.20},
        {"id": 6, "name": "Interior Wall Paint (5 Gal)", "sku": "PAINT-INT-5G", "category": "Paint", "supplier_id": 5, "quantity": 220, "reorder_level": 50, "unit_cost": 85.00},
        {"id": 7, "name": "Exterior Wall Paint (5 Gal)", "sku": "PAINT-EXT-5G", "category": "Paint", "supplier_id": 5, "quantity": 180, "reorder_level": 40, "unit_cost": 92.50},
        {"id": 8, "name": "Lumber 2x4 (8ft)", "sku": "LUM-2X4-8", "category": "Wood", "supplier_id": 3, "quantity": 1000, "reorder_level": 200, "unit_cost": 5.75},
        {"id": 9, "name": "Gravel (per cubic yard)", "sku": "GRV-CY", "category": "Building Materials", "supplier_id": 1, "quantity": 75, "reorder_level": 20, "unit_cost": 28.00},
        {"id": 10, "name": "Sand (per cubic yard)", "sku": "SND-CY", "category": "Building Materials", "supplier_id": 1, "quantity": 90, "reorder_level": 25, "unit_cost": 20.00},
    ]
    Material.objects.bulk_create([Material(**m) for m in materials])

def unseed_data(apps, schema_editor):
    Supplier = apps.get_model('inventory', 'Supplier')
    Material = apps.get_model('inventory', 'Material')
    Material.objects.all().delete()
    Supplier.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),  # replace with your initial migration
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
