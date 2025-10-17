from django.urls import path
from . import views_web

urlpatterns = [
    path("materials", views_web.material_list, name="material_list"),
    path("suppliers/create", views_web.supplier_create, name="supplier_create"),
    path("materials/create", views_web.material_create, name="material_create"),
    path("materials/<int:pk>/edit/", views_web.material_update, name="material_update"),
    path("materials/<int:pk>/update_stock/", views_web.update_stock, name="update_stock"),
    path("materials/<int:pk>/delete", views_web.material_delete, name="material_delete"),
    path("", views_web.dashboard, name="dashboard"),
]