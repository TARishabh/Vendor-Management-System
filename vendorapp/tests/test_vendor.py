from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Vendor
class VendorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor1 = Vendor.objects.create(
            name='Vendor 1',
            contact_details='9234567890',
            address='Address 1',
            vendor_code='vendor1code'
        )

    def test_get_vendor_list(self):
        response = self.client.get(reverse('vendor-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_vendor(self):
        # Invalid contact details
        invalid_data = {
            'name': 'New Vendor',
            'contact_details': '1234567890',  # Invalid contact details
            'address': 'New Address'
        }
        response = self.client.post(reverse('vendor-list-create'), invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Valid contact details
        valid_data = {
            'name': 'New Vendor',
            'contact_details': '9876543210',
            'address': 'New Address'
        }
        response = self.client.post(reverse('vendor-list-create'), valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_get_vendor_detail(self):
        response = self.client.get(reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Vendor 1')

    def test_update_vendor(self):
        data = {'name': 'Updated Vendor'}
        response = self.client.patch(reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor1.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Vendor')

    def test_delete_vendor(self):
        response = self.client.delete(reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)
