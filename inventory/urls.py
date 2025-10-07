from django.urls import path
from . import views

urlpatterns = [
    path("materials", views.material_list, name="material_list"),
    path("suppliers/create", views.supplier_create, name="supplier_create"),
    path("materials/create", views.material_create, name="material_create"),
    path("materials/<int:pk>/edit/", views.material_update, name="material_update"),
    path("materials/<int:pk>/update_stock/", views.update_stock, name="update_stock"),
    path("materials/<int:pk>/delete", views.material_delete, name="material_delete"),
    path("", views.dashboard, name="dashboard"),
]