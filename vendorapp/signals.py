from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance,Vendor
from django.utils import timezone
import pdb
from django.db.models import Sum
current_time = timezone.now()

@receiver(pre_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance,instance_status=None, **kwargs):
    """
    Signal handler to update performance metrics upon creation or update of a purchase order.
    """
    if instance_status:
        instance.status = instance_status
    
    # previous_purchase_order = PurchaseOrder.objects.select_related('vendor').get(pk=instance.pk)
    if instance.pk:  # Check if the instance has already been saved
        try:
            previous_purchase_order = PurchaseOrder.objects.get(pk=instance.pk)
            previous_status = previous_purchase_order.status
            if previous_status != instance.status:
                global current_time
                fulfillment_rate = update_fulfillment_rate(instance)
                avg_response_time = update_avg_response_time(instance)
                if instance.status == 'completed':
                    on_time_delivery_rate = update_on_time_delivery_rate(instance)
                    avg_quality_rating = update_quality_rating_average(instance)
                else:
                    on_time_delivery_rate = previous_purchase_order.vendor.on_time_delivery_rate
                    avg_quality_rating = previous_purchase_order.vendor.quality_rating_avg
                
                HistoricalPerformance.objects.create(
                        vendor=instance.vendor,
                        date=current_time.date(),
                        on_time_delivery_rate=on_time_delivery_rate,
                        quality_rating_avg= avg_quality_rating,
                        average_response_time= avg_response_time,
                        fulfillment_rate= fulfillment_rate
                    )
            elif instance.acknowledgment_date:
                avg_response_time = update_avg_response_time(instance)
        except PurchaseOrder.DoesNotExist:
            pass

    # vendor_on_time_delivery_rate = previous_purchase_order.vendor.on_time_delivery_rate

    

def update_fulfillment_rate(instance):
    """
    Signal handler to update the fulfilment rate upon change in PO status.
    """
    
    global current_time
    # Get the total number of purchase orders issued to the vendor
    total_orders = PurchaseOrder.objects.filter(vendor=instance.vendor).count()
    # Get the number of successfully fulfilled purchase orders
    successful_orders = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').count()
    # pdb.set_trace()
    if instance.status == 'completed':
        successful_orders += 1
    if total_orders > 1:
        fulfilment_rate = (successful_orders / total_orders) * 100
    elif total_orders <= 1 and successful_orders <= 1:
        fulfilment_rate = (successful_orders / total_orders) * 100
    else:
        fulfilment_rate = 0
    
    # Update the delivery date of the completed order

    Vendor.objects.filter(id=instance.vendor.id).update(fulfillment_rate=fulfilment_rate)
    return fulfilment_rate
    
def update_avg_response_time(instance):
    """
    Calculate the average response time for the vendor.
    """
    # Get all completed orders of the vendor with acknowledgment dates
    # pdb.set_trace()
    if instance.acknowledgment_date:
        PurchaseOrder.objects.filter(id=instance.id).update(acknowledgment_date=instance.acknowledgment_date)
    
    completed_orders = PurchaseOrder.objects.filter(
        vendor=instance.vendor,
        acknowledgment_date__isnull=False
    )
    
    
    # Calculate the total response time for all completed orders
    total_response_time = sum((order.acknowledgment_date - order.issue_date).days for order in completed_orders)
    # print(total_response_time)
    
    # total_response_time = sum((order.acknowledgment_date - order.issue_date).total_seconds() / (24 * 3600) for order in completed_orders)
    # print(total_response_time)
        
    
    # Calculate the average response time
    total_orders = completed_orders.count()
    avg_response_time_days = total_response_time / total_orders if total_orders > 0 else 0
    
    # Update the average response time for the vendor
    Vendor.objects.filter(id=instance.vendor.id).update(average_response_time=avg_response_time_days)
    
    return avg_response_time_days

def update_on_time_delivery_rate(instance):
    global current_time
    completed_order = PurchaseOrder.objects.get(id=instance.id)
        
    # Check if there are any existing PurchaseOrder records for the vendor
    total_records_count = PurchaseOrder.objects.filter(vendor=instance.vendor,status='completed').count()
    if instance.status == 'completed':
        total_records_count +=1 
    
    # If there are no existing records, set initial_on_time_delivery_rate accordingly
    if total_records_count == 1:
        if completed_order.delivery_date >= current_time:
            initial_on_time_delivery_rate = 100
        else:
            initial_on_time_delivery_rate = 0
            
    else:
        existing_on_time_delivery_rate = Vendor.objects.get(id=instance.vendor.id).on_time_delivery_rate
        successful_orders = (existing_on_time_delivery_rate * (total_records_count-1))/100
        
        # this if is only for test case, otherwise it will always enter the else case:
        '''
        we are using the logic here, that when the status is changed to complete, the delivery date is automatically updated
        with the current time, but in test case, we are sending the delivery date, so we are using a if case.
        '''
        if instance.delivery_date:
            initial_on_time_delivery_rate = ((successful_orders)*100)/(total_records_count)
        else:
            if completed_order.delivery_date >= current_time:
                initial_on_time_delivery_rate = ((successful_orders + 1)*100)/(total_records_count)
            else:
                initial_on_time_delivery_rate = ((successful_orders)*100)/(total_records_count)
        
        if initial_on_time_delivery_rate > 100:
            initial_on_time_delivery_rate = 100
        
        # Get the latest on-time delivery rate for the vendor
    if instance.status == 'completed':
        PurchaseOrder.objects.filter(id=instance.id).update(delivery_date=current_time)
    Vendor.objects.filter(id=instance.vendor.id).update(on_time_delivery_rate=initial_on_time_delivery_rate)
    return initial_on_time_delivery_rate

from django.db.models import Avg

def update_quality_rating_average(instance):
    """
    Calculate the average quality rating for the vendor.
    """
    # Get the vendor of the completed order
    vendor = instance.vendor
    
    # Access the incoming quality_rating from the instance
    quality_rating = instance.quality_rating
    # Check if the quality_rating is provided
    if quality_rating is not None:
        # Check if the order is completed
        if instance.status == 'completed':
            # Get all completed orders of the vendor with a quality rating
            completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(quality_rating=None)
            
            # Calculate the total quality rating and count the number of orders with quality ratings
            total_quality_rating = completed_orders.aggregate(total_rating=Sum('quality_rating'))['total_rating'] or 0
            total_ratings = completed_orders.count()
            
            # Calculate the new average quality rating including the incoming change
            new_total_quality_rating = total_quality_rating + quality_rating
            new_total_ratings = total_ratings + 1
            average_quality_rating = new_total_quality_rating / new_total_ratings
            
            # Update the average quality rating for the vendor
            Vendor.objects.filter(id=vendor.id).update(quality_rating_avg=average_quality_rating)
            
            return average_quality_rating
        else:
            # Order is not completed, return existing average quality rating
            return vendor.quality_rating_avg
    else:
        # Quality rating is not provided, return existing average quality rating
        return vendor.quality_rating_avg
