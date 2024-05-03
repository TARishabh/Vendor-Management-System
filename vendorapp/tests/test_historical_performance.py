from django.test import TestCase
from django.utils import timezone
from ..models import HistoricalPerformance, Vendor,PurchaseOrder
from ..signals import update_performance_metrics
from datetime import datetime, timedelta

class HistoricalPerformanceModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='9234567890',
            address='Test Address',
            vendor_code='VENDOR123'
        )
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=datetime.now(),
            delivery_date=datetime.now() + timedelta(days=7),
            items=['Item 1', 'Item 2'],
            quantity=10,
            status='NA',  # Set status to 'NA' initially (NOT ACKNOWLEDGED)
            quality_rating=4.5,
            issue_date=datetime.now(),
            acknowledgment_date=None,  # Assuming acknowledgment date is None initially
        )

    def test_historical_performance_creation(self):
        # Trigger the signal for the pending status
        update_performance_metrics(None, instance=self.purchase_order)
        # Check if one instance is created for the pending status
        self.assertEqual(HistoricalPerformance.objects.count(), 0)

        # Update the purchase order status to 'completed'
        self.purchase_order.status = 'completed'
        self.purchase_order.save()

        # Trigger the signal again for the completed status
        update_performance_metrics(None, instance=self.purchase_order)
        # Check if another instance is created for the completed status
        self.assertEqual(HistoricalPerformance.objects.count(), 1)
