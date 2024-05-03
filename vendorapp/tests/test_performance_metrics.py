import pdb
from django.urls import reverse
from django.utils import timezone
from ..models import Vendor, PurchaseOrder, HistoricalPerformance
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta,datetime
import json
from ..signals import update_performance_metrics


class PerformanceMetricTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='1234567890',
            address='Test Address',
            vendor_code='VENDOR123'
        )

    def test_performance_metric(self):
        # Step 1: Create a purchase order with 'NA' status and issue date set to the current date
        items_data = [
            {
                "name": "Product A",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "quantity": 10,
                "unit_price": 20.50
            },
            {
                "name": "Product B",
                "description": "Nulla nec nisl eget urna commodo condimentum.",
                "quantity": 5,
                "unit_price": 15.75
            },
            {
                "name": "Product C",
                "description": "Sed quis lacus vel elit vehicula suscipit.",
                "quantity": 8,
                "unit_price": 30.00
            }
        ]

        # Step 1: Create a purchase order with 'NA' status and issue date set to the current date
        response = self.client.post(reverse('purchaseorder-list-create'), {
            'items': json.dumps(items_data),
            'quantity': 3,
            'status': 'NA'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        purchase_order = PurchaseOrder.objects.get(pk=response.data['id'])

        # # Print all fields of the PurchaseOrder object
        # print("ID:", purchase_order.id)
        # print("PO Number:", purchase_order.po_number)
        # print("Vendor:", purchase_order.vendor)
        # print("Order Date:", purchase_order.order_date)
        # print("Delivery Date:", purchase_order.delivery_date)
        # print("Items:", purchase_order.items)
        # print("Quantity:", purchase_order.quantity)
        # print("Status:", purchase_order.status)
        # print("Quality Rating:", purchase_order.quality_rating)
        # print("Issue Date:", purchase_order.issue_date)
        # print("Acknowledgment Date:", purchase_order.acknowledgment_date)
        purchase_order_id = response.data['id']

        # Step 2: Assign the purchase order to the vendor and update the issue date
        purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
        purchase_order.vendor = self.vendor
        purchase_order.issue_date = timezone.now()
        purchase_order.save()

        
        current_date = datetime.now()

        # Add 3 days to the current date to get the acknowledgment date
        acknowledgment_date = current_date + timedelta(days=3)

        # Format acknowledgment date as a string compatible with ISO 8601 format
        acknowledgment_date_iso = acknowledgment_date.strftime('%Y-%m-%dT%H:%M:%S')

        # Step 3: Acknowledge the purchase order by the vendor, which changes status to 'Pending'
        response = self.client.post(
            reverse('purchase-order-acknowledge', kwargs={'po_id': purchase_order_id}),
            data={'acknowledgment_date': acknowledgment_date_iso}
        )

        # Retrieve the purchase order object
        purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)

        # Modify the status attribute of the purchase order object
        purchase_order.status = 'pending'

        # Save the modified purchase order object
        purchase_order.save()

        # Check if the response status code is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Step 4: Check performance metrics before status update
        performance_metric_before = HistoricalPerformance.objects.last()
        # pdb.set_trace()
        self.assertEqual(performance_metric_before.on_time_delivery_rate, 0.0)
        self.assertEqual(performance_metric_before.quality_rating_avg, 0.0)
        self.assertEqual(performance_metric_before.average_response_time, 3.0)
        self.assertEqual(performance_metric_before.fulfillment_rate, 0.0)

        # Step 5: Mark the order as completed and update the delivery date
        purchase_order.status = 'completed'
        purchase_order.delivery_date = timezone.now() - timedelta(days=2)  # Less than expected delivery date
        purchase_order.save()

        # Step 6: Check performance metrics after status update
        performance_metric_after = HistoricalPerformance.objects.last()
        self.assertEqual(performance_metric_after.on_time_delivery_rate, 100.0)
        self.assertEqual(performance_metric_after.quality_rating_avg, 0.0)
        self.assertEqual(performance_metric_after.average_response_time, 3.0)
        self.assertEqual(performance_metric_after.fulfillment_rate, 100.0)

        
        # Step 7: Create a another purchase order with 'NA' status 
        response = self.client.post(reverse('purchaseorder-list-create'), {
            'items': json.dumps(items_data),
            'quantity': 3,
            'status': 'NA'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        purchase_order = PurchaseOrder.objects.get(pk=response.data['id'])
        purchase_order_id = response.data['id']

        # Step 8: Assign the purchase order to the vendor and update the issue date
        purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
        purchase_order.vendor = self.vendor
        purchase_order.issue_date = timezone.now()
        purchase_order.save()

        
        current_date = datetime.now()

        # Add 5 days to the current date to get the acknowledgment date
        acknowledgment_date = current_date + timedelta(days=5)

        # Format acknowledgment date as a string compatible with ISO 8601 format
        acknowledgment_date_iso = acknowledgment_date.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Step 9: Acknowledge the purchase order by the vendor, which changes status to 'Pending'
        response = self.client.post(
            reverse('purchase-order-acknowledge', kwargs={'po_id': purchase_order_id}),
            data={'acknowledgment_date': acknowledgment_date_iso}
        )

        # Retrieve the purchase order object
        purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)

        # Modify the status attribute of the purchase order object
        purchase_order.status = 'pending'

        # Save the modified purchase order object
        purchase_order.save()

        # Check if the response status code is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Step 10: Check performance metrics before status update
        performance_metric_before = HistoricalPerformance.objects.last()
        # pdb.set_trace()
        self.assertEqual(performance_metric_before.on_time_delivery_rate, 100.0)
        self.assertEqual(performance_metric_before.quality_rating_avg, 0.0)
        self.assertEqual(performance_metric_before.average_response_time, 4.0)
        self.assertEqual(performance_metric_before.fulfillment_rate, 50.0)
        
        # Step 11: Mark the order as completed and update the delivery date
        purchase_order.status = 'completed'
        purchase_order.delivery_date = purchase_order.order_date + timedelta(days=10)  # Later than expected delivery date
        purchase_order.quality_rating = 3  # Set the quality rating to 3
        purchase_order.save()

        # Step 12: Check performance metrics after status update
        performance_metric_after = HistoricalPerformance.objects.last()
        self.assertEqual(performance_metric_after.on_time_delivery_rate, 50.0)
        self.assertEqual(performance_metric_after.quality_rating_avg, 3.0)
        self.assertEqual(performance_metric_after.average_response_time, 4.0)
        self.assertEqual(performance_metric_after.fulfillment_rate, 100.0)
        
        # Step 13: Now, check the vendor's performance metrics:
        response = self.client.get(reverse('vendor_performance', kwargs={'vendor_id': self.vendor.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        performance_metrics = response.data

        # Assert the vendor's performance metrics
        self.assertEqual(performance_metrics['on_time_delivery_rate'], 50.0)
        self.assertEqual(performance_metrics['quality_rating_avg'], 3.0)
        self.assertEqual(performance_metrics['average_response_time'], 4.0)
        self.assertEqual(performance_metrics['fulfillment_rate'], 100.0)
        
        # Step 14: Create a new acknowledgment date
        current_date = datetime.now()
        acknowledgment_date = current_date + timedelta(days=7)
        acknowledgment_date_iso = acknowledgment_date.strftime('%Y-%m-%dT%H:%M:%S')

        # Step 15: Acknowledge the purchase order again with the new acknowledgment date
        response = self.client.post(
            reverse('purchase-order-acknowledge', kwargs={'po_id': purchase_order_id}),
            data={'acknowledgment_date': acknowledgment_date_iso}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Step 16: Check if the acknowledgment date is updated and triggers recalculation of average_response_time
        purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
        self.assertEqual(purchase_order.acknowledgment_date.date(), acknowledgment_date.date())
        
        # Step 17: Now, check the vendor's performance metrics:
        response = self.client.get(reverse('vendor_performance', kwargs={'vendor_id': self.vendor.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        performance_metrics = response.data

        # Assert the vendor's performance metrics
        self.assertEqual(performance_metrics['on_time_delivery_rate'], 50.0)
        self.assertEqual(performance_metrics['quality_rating_avg'], 3.0)
        self.assertEqual(performance_metrics['average_response_time'], 5.0) # avg response time updated to (7+3)/2 = 5
        self.assertEqual(performance_metrics['fulfillment_rate'], 100.0)