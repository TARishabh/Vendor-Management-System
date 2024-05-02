from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance,Vendor
from django.utils import timezone
import pdb
from django.db.models import ExpressionWrapper, F, Func, Value, IntegerField,Avg,Sum
from datetime import date

# Sure, here's how you can update the logic to either create a new HistoricalPerformance row or update an existing one based on the date:

current_time = timezone.now()

@receiver(pre_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, **kwargs):
    """
    Signal handler to update performance metrics upon creation or update of a purchase order.
    """
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
                
                # pdb.set_trace()
                HistoricalPerformance.objects.create(
                        vendor=instance.vendor,
                        date=current_time.date(),
                        on_time_delivery_rate=on_time_delivery_rate,
                        quality_rating_avg= avg_quality_rating,
                        average_response_time= avg_response_time,
                        fulfillment_rate= fulfillment_rate
                    )
        except PurchaseOrder.DoesNotExist:
            # Handle the case where the previous purchase order does not exist
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
    if total_orders > 0:
        fulfilment_rate = (successful_orders / total_orders) * 100
    else:
        fulfilment_rate = 0
    
    # Update the delivery date of the completed order
    PurchaseOrder.objects.filter(id=instance.id).update(delivery_date=current_time)
    Vendor.objects.filter(id=instance.vendor.id).update(fulfillment_rate=fulfilment_rate)
    return fulfilment_rate
    
def update_avg_response_time(instance):
    """
    Calculate the average response time for the vendor.
    """
    # Get all completed orders of the vendor with acknowledgment dates
    completed_orders = PurchaseOrder.objects.filter(
        vendor=instance.vendor,
        acknowledgment_date__isnull=False
    )
    # pdb.set_trace()
    
    # Calculate the total response time for all completed orders
    # total_response_time = sum((order.acknowledgment_date - order.issue_date).days for order in completed_orders)
    response_time = []
    for order in completed_orders:
        print((order.acknowledgment_date - order.issue_date).days)
        response_time.append((order.acknowledgment_date - order.issue_date).days)
    
    total_response_time = sum(response_time)
    print(total_response_time)
    
    
    # Calculate the average response time
    total_orders = completed_orders.count()
    avg_response_time_days = total_response_time / total_orders if total_orders > 0 else None
    
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
    # pdb.set_trace()
    
    # If there are no existing records, set initial_on_time_delivery_rate accordingly
    if total_records_count == 1:
        if completed_order.delivery_date >= current_time:
            initial_on_time_delivery_rate = 100
        else:
            initial_on_time_delivery_rate = 0
            
    else:
        existing_on_time_delivery_rate = Vendor.objects.get(id=instance.vendor.id).on_time_delivery_rate
        successful_orders = (existing_on_time_delivery_rate * (total_records_count))/100
        if completed_order.delivery_date >= current_time:
            initial_on_time_delivery_rate = ((successful_orders + 1)*100)/(total_records_count)
        else:
            initial_on_time_delivery_rate = ((successful_orders)*100)/(total_records_count)
        
        if initial_on_time_delivery_rate > 100:
            initial_on_time_delivery_rate = 100
        
        # Get the latest on-time delivery rate for the vendor
    # on_time_delivery_rate = initial_on_time_delivery_rate if initial_on_time_delivery_rate else existing_on_time_delivery_rate
    Vendor.objects.filter(id=instance.vendor.id).update(on_time_delivery_rate=initial_on_time_delivery_rate)
    return initial_on_time_delivery_rate

def update_quality_rating_average(instance):
    # Get the vendor of the completed order
    vendor = instance.vendor
    
    # Get all completed orders of the vendor with a quality rating
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(quality_rating=None)
    
    # Calculate the total quality rating and count the number of orders with quality ratings
    total_quality_rating = 0
    total_ratings = 0
    for order in completed_orders:
        if order.quality_rating is not None:
            total_quality_rating += order.quality_rating
            total_ratings += 1
    
    # Calculate the average quality rating
    average_quality_rating = total_quality_rating / total_ratings if total_ratings > 0 else 0
    average_quality_rating = 5
    return average_quality_rating
    
    
    
    
    
    
    
#     quality_rating_avg = 4.5
#     average_response_time = 12.5
#     fulfillment_rate = 95.0
#     if instance.status == 'completed':
#         completed_order = PurchaseOrder.objects.get(id=instance.id)
#         current_time = timezone.now()
#         # pdb.set_trace()
#         # Check if there are any existing HistoricalPerformance records for the vendor
#         existing_records_count = HistoricalPerformance.objects.filter(vendor=instance.vendor).count()
#         print(existing_records_count,'existing_records_count')

#         # If there are no existing records, set initial_on_time_delivery_rate accordingly
#         if existing_records_count == 0:
#             if completed_order.delivery_date >= current_time:
#                 initial_on_time_delivery_rate = 100
#             else:
#                 initial_on_time_delivery_rate = 0

#             HistoricalPerformance.objects.create(
#                 vendor=instance.vendor,
#                 date=current_time.date(),
#                 on_time_delivery_rate=initial_on_time_delivery_rate,
#                 quality_rating_avg= quality_rating_avg,
#                 average_response_time= average_response_time,
#                 fulfillment_rate= fulfillment_rate
#             )
#         else:
#             # Get the latest on-time delivery rate for the vendor
#             latest_on_time_delivery_rate = HistoricalPerformance.objects.filter(vendor=instance.vendor).order_by('-id').first().on_time_delivery_rate
#             print(latest_on_time_delivery_rate,'latest_on_time_delivery_rate')
#             # Calculate the successful delivery count
#             successful_delivery_count = latest_on_time_delivery_rate * existing_records_count / 100
#             print(successful_delivery_count,'successful_delivery_count')
#             # Update existing records count and successful delivery count based on the current order
#             if completed_order.delivery_date >= current_time:
#                 successful_delivery_count = successful_delivery_count + 1
#                 existing_records_count = existing_records_count + 1
#             else:
#                 print('yes i am in else')
#                 existing_records_count = existing_records_count + 1
            
#             # Calculate the new on-time delivery rate
#             new_on_time_delivery_rate = (successful_delivery_count / existing_records_count) * 100
#             print(new_on_time_delivery_rate)
#             # Create or update HistoricalPerformance record
#             HistoricalPerformance.objects.create(
#                 vendor=instance.vendor,
#                 date=current_time.date(),
#                 on_time_delivery_rate=new_on_time_delivery_rate,
#                 quality_rating_avg= quality_rating_avg,
#                 average_response_time= average_response_time,
#                 fulfillment_rate= fulfillment_rate
#             )
#         # Update the delivery date of the completed order
#         PurchaseOrder.objects.filter(id=instance.id).update(delivery_date=current_time)

# @receiver(post_save, sender=PurchaseOrder)
# def update_fulfilment_rate(sender, instance, created, **kwargs):
#     """
#     Signal handler to update the fulfilment rate upon creation or update of a purchase order.
#     """
#     if not created:
#         # Get the previous status using the primary key (pk)
#         previous_status = PurchaseOrder.objects.get(pk=instance.pk).status

#         if previous_status != instance.status:
#             current_time = timezone.now()
#             # Get the total number of purchase orders issued to the vendor
#             total_orders = PurchaseOrder.objects.filter(vendor=instance.vendor).count()
            
#             # Get the number of successfully fulfilled purchase orders
#             successful_orders = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').count()
            
#             # Calculate the fulfilment rate
#             if total_orders > 0:
#                 fulfilment_rate = (successful_orders / total_orders) * 100
#             else:
#                 fulfilment_rate = 0
            
#             previous_details =  HistoricalPerformance.objects.filter(vendor=instance.vendor)
#             if previous_details.exists():
#                 latest_performance = previous_details.latest('date')
#                 quality_rating_avg = latest_performance.quality_rating_avg
#                 average_response_time = latest_performance.average_response_time
#                 on_time_delivery_rate = latest_performance.on_time_delivery_rate
#             else:
#                 quality_rating_avg = 0.0
#                 average_response_time = 0.0
#                 on_time_delivery_rate = 0.0
            
#             # Create or update HistoricalPerformance record
#             HistoricalPerformance.objects.create(
#                 vendor=instance.vendor,
#                 date=current_time.date(),
#                 on_time_delivery_rate=on_time_delivery_rate,
#                 quality_rating_avg= quality_rating_avg,
#                 average_response_time= average_response_time,
#                 fulfillment_rate= fulfilment_rate
#             )

# # Prevent recursion by excluding fulfilment_rate field from triggering the post_save signal
# # instance.save(update_fields=['status'])

# if status is changed:
# fulfilment rate, but if the status is changed only to completed then on_time_deli_rate is also called, if quality rating is also given then Quality Rating Average


# hierarchy:
# FullFillment (triggered everytime when status changes)
# |
# v
# Average Response Time:(when status changes to cancel or pending)
# |
# v
# On-Time Delivery Rate == Quality Rating Average: (when status is changed to completed)

