from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance
from django.utils import timezone
import pdb
from django.db.models import F
from django.db.models import Count


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, created, **kwargs):
    """
    Signal handler to update performance metrics upon creation or update of a purchase order.
    """
    quality_rating_avg = 4.5
    average_response_time = 12.5
    fulfillment_rate = 95.0
    if instance.status == 'completed':
        completed_order = PurchaseOrder.objects.get(id=instance.id)
        current_time = timezone.now()
        # pdb.set_trace()
        # Check if there are any existing HistoricalPerformance records for the vendor
        existing_records_count = HistoricalPerformance.objects.filter(vendor=instance.vendor).count()
        print(existing_records_count,'existing_records_count')

        # If there are no existing records, set initial_on_time_delivery_rate accordingly
        if existing_records_count == 0:
            if completed_order.delivery_date >= current_time:
                initial_on_time_delivery_rate = 100
            else:
                initial_on_time_delivery_rate = 0

            HistoricalPerformance.objects.create(
                vendor=instance.vendor,
                date=current_time.date(),
                on_time_delivery_rate=initial_on_time_delivery_rate,
                quality_rating_avg= quality_rating_avg,
                average_response_time= average_response_time,
                fulfillment_rate= fulfillment_rate
            )
        else:
            # Get the latest on-time delivery rate for the vendor
            latest_on_time_delivery_rate = HistoricalPerformance.objects.filter(vendor=instance.vendor).order_by('-id').first().on_time_delivery_rate
            print(latest_on_time_delivery_rate,'latest_on_time_delivery_rate')
            # Calculate the successful delivery count
            successful_delivery_count = latest_on_time_delivery_rate * existing_records_count / 100
            print(successful_delivery_count,'successful_delivery_count')
            # Update existing records count and successful delivery count based on the current order
            if completed_order.delivery_date >= current_time:
                successful_delivery_count = successful_delivery_count + 1
                existing_records_count = existing_records_count + 1
            else:
                print('yes i am in else')
                existing_records_count = existing_records_count + 1
            
            # Calculate the new on-time delivery rate
            new_on_time_delivery_rate = (successful_delivery_count / existing_records_count) * 100
            print(new_on_time_delivery_rate)
            # Create or update HistoricalPerformance record
            HistoricalPerformance.objects.create(
                vendor=instance.vendor,
                date=current_time.date(),
                on_time_delivery_rate=new_on_time_delivery_rate,
                quality_rating_avg= quality_rating_avg,
                average_response_time= average_response_time,
                fulfillment_rate= fulfillment_rate
            )
        # Update the delivery date of the completed order
        PurchaseOrder.objects.filter(id=instance.id).update(delivery_date=current_time)

        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # print(instance.status)
        # # Step 1: Get all completed purchase orders for the vendor
        # completed_pos = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed')
        # print(completed_pos)

        # # Step 2: Count the number of completed POs delivered on or before each PO's delivery date
        # on_time_delivered_pos_count = 0
        # total_completed_pos_count = 0
        # for po in completed_pos:
        #     print(timezone.now())
        #     print(po.delivery_date)
        #     print(po.delivery_date >= timezone.now())
        #     if po.delivery_date >= timezone.now():
        #         print('yesss')
        #         on_time_delivered_pos_count += 1
        #     total_completed_pos_count += 1

        # # Step 3: Calculate the on-time delivery rate for the vendor
        # if total_completed_pos_count > 0:
        #     on_time_delivery_rate = (on_time_delivered_pos_count / total_completed_pos_count) * 100
        # else:
        #     on_time_delivery_rate = 0

        # # Hardcoded values for demonstration purposes
        # quality_rating_avg = 4.5
        # average_response_time = 12.5
        # fulfillment_rate = 95.0

        # # Step 4: Create or update historical performance record
        # HistoricalPerformance.objects.update_or_create(
        #     vendor=instance.vendor,
        #     date=instance.delivery_date.date(),
        #     defaults={
        #         'on_time_delivery_rate': on_time_delivery_rate,
        #         'quality_rating_avg': quality_rating_avg,
        #         'average_response_time': average_response_time,
        #         'fulfillment_rate': fulfillment_rate
        #     }
        # )
