from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from sqlparse.engine.grouping import group

from .models import Material, Supplier, MaterialCategory


class MaterialAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test-manager', password='testman123')
        from rest_framework_simplejwt.tokens import RefreshToken
        token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')


        # Create test supplier and category
        self.supplier = Supplier.objects.create(name="ACME Tools")
        self.category = MaterialCategory.objects.create(name="Hardware")

        # Base URLs
        self.list_url = reverse('materials-list')
        self.create_url = reverse('materials-add')

    def test_create_material(self):
        """POST: create a material"""
        data = {
            'sku': 'MAT-001',
            'name': 'Cement Bags',
            'category': self.category.id,
            'supplier': self.supplier.id,
            'quantity': 100,
            'unit_cost': '9.99'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Material.objects.count(), 11)
        self.assertEqual(Material.objects.first().name, 'Cement Bags')

    def test_get_materials(self):
        """GET: list materials"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_update_material(self):
        """PUT: update material"""
        material = Material.objects.create(sku='MAT-003', name='Sand', category=self.category, supplier=self.supplier,
                                           quantity=20, unit_cost=2.50)
        url = reverse('materials-detail', kwargs={'pk': material.id})
        response = self.client.put(url, {'name': 'Fine Sand', 'sku': 'MAT-003', 'category': self.category.id,
                                         'supplier': self.supplier.id, 'quantity': 30, 'unit_cost': 3.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        material.refresh_from_db()
        self.assertEqual(material.name, 'Fine Sand')

    def test_delete_material(self):
        """DELETE: remove material"""
        material = Material.objects.create(sku='MAT-004', name='Paint', category=self.category, supplier=self.supplier,
                                           quantity=10, unit_cost=12.00)
        url = reverse('materials-detail', kwargs={'pk': material.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Material.objects.filter(id=material.id).exists())
