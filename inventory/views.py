from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import SupplierForm, MaterialForm
from django.db.models import Sum
from .models import Material

def material_list(request):
    materials = Material.objects.all()
    return render(request, "inventory/material_list.html", {"materials": materials})

def supplier_create(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("material_list")
    else:
        form = SupplierForm()
    return render(request, "inventory/supplier_form.html", {"form": form})

def material_create(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("material_list")
    else:
        form = MaterialForm()
    return render(request, "inventory/material_form.html", {"form": form})

def material_update(request, pk):
    material = get_object_or_404(Material, pk=pk)  # Load existing material

    if request.method == "POST":
        form = MaterialForm(request.POST, instance=material)  # Bind to existing instance
        if form.is_valid():
            form.save()
            return redirect("material_list")
    else:
        form = MaterialForm(instance=material)  # Pre-populate form

    return render(request, "inventory/material_form.html", {"form": form, "material": material})

def material_delete(request, pk):
    if request.method == "POST":
        material = get_object_or_404(Material, pk=pk)
        material.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

def update_stock(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if request.method == "POST":
        qty_str = request.POST.get("quantity")
        if qty_str is None:
            return JsonResponse({"success": False, "error": "Quantity not provided"}, status=400)

        try:
            new_qty = int(qty_str)
        except ValueError:
            return JsonResponse({"success": False, "error": "Quantity must be an integer"}, status=400)

        if new_qty < 0:
            return JsonResponse({"success": False, "error": "Quantity cannot be negative"}, status=400)

        material.quantity = new_qty
        material.save()
        return JsonResponse({"success": True, "quantity": material.quantity})

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


def dashboard(request):
    # get stock counts
    in_stock_count = Material.objects.filter(quantity__gt=models.F('reorder_level')).count()
    low_stock_count = Material.objects.filter(quantity__lte=models.F('reorder_level')).count()
    out_of_stock_count = Material.objects.filter(quantity=0).count()

    top_materials = Material.objects.order_by('-quantity')[:10]

    # Prepare labels and data as Python lists
    top_materials_dict = {m.name:m.quantity for m in top_materials}

    # Category counts
    category_counts = Material.objects.values('category').annotate(sum=Sum('quantity')).order_by('-sum')
    category_dict = {c['category']: c['sum'] for c in category_counts}

    # Top suppliers
    supplier_counts = Material.objects.values('supplier__name').annotate(sum=Sum('quantity')).order_by('-sum')
    supplier_dict = {s['supplier__name'] if s['supplier__name'] else 'Unknown': s['sum'] for s in
                     supplier_counts}

    return render(request, 'inventory/dashboard.html', {
        'in_stock_count': in_stock_count,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'category_counts': category_dict,
        'supplier_counts': supplier_dict,
        'top_material_counts': top_materials_dict,
    })
