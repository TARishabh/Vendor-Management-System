from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import PurchaseOrder, Vendor
from datetime import datetime, timedelta
import json

class PurchaseOrderAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name='Vendor 1',
            contact_details='9234567890',
            address='Address 1',
        )
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=datetime.now(),
            delivery_date=datetime.now() + timedelta(days=7),
            items=json.dumps(['Item 1', 'Item 2']),
            quantity=10,
            status='NA',
            quality_rating=None,
            issue_date=datetime.now(),
            acknowledgment_date=None
        )

    def test_get_purchase_order_list(self):
        response = self.client.get(reverse('purchaseorder-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_purchase_order(self):
        data = {
            'po_number': 'PO002',
            'vendor': self.vendor.id,
            'items': ['Item 3', 'Item 4'],
            'quantity': 5,
        }
        response = self.client.post(reverse('purchaseorder-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_get_purchase_order_detail(self):
        response = self.client.get(reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], 'PO001')

    def test_update_purchase_order(self):
        data = {'status': 'completed'}
        response = self.client.patch(reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

    def test_delete_purchase_order(self):
        response = self.client.delete(reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)
