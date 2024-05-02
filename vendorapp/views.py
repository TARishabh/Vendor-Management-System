from rest_framework import generics
from .models import Vendor,PurchaseOrder
from .serializers import VendorPostSerializer,VendorRetrieveSerializer,PurchaseOrderCreateUpdateSerializer,PurchaseOrderDetailSerializer,PurchaseOrderUpdateSerializer,PurchaseOrderAcknowledgeSerializer
from .models import Vendor, HistoricalPerformance
from .serializers import HistoricalPerformanceSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import VendorPerformanceSerializer
from rest_framework import status
from django.utils import timezone



class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    def get_serializer_class(self):
        """
        Selects the appropriate serializer based on the request method.
        """
        if self.request.method == 'POST':
            return VendorPostSerializer
        return VendorRetrieveSerializer

class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    def get_serializer_class(self):
        """
        Selects the appropriate serializer based on the request method.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return VendorPostSerializer
        return VendorRetrieveSerializer
    
class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    def get_serializer_class(self):
        """
        Selects the appropriate serializer based on the request method.
        """
        if self.request.method == 'POST':
            return PurchaseOrderCreateUpdateSerializer
        return PurchaseOrderDetailSerializer

class PurchaseOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    def get_serializer_class(self):
        """
        Selects the appropriate serializer based on the request method.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return PurchaseOrderUpdateSerializer
        return PurchaseOrderDetailSerializer
    
# class VendorPerformanceView(generics.RetrieveAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = HistoricalPerformanceSerializer

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         historical_performance = HistoricalPerformance.objects.filter(vendor=instance)
#         serializer = self.get_serializer(historical_performance, many=True)
#         return Response(serializer.data)

class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            serializer = VendorPerformanceSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PurchaseOrderAcknowledgeView(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PurchaseOrderAcknowledgeSerializer(purchase_order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Trigger recalculation of average_response_time
            # Call the function or signal to recalculate average_response_time
            # For example: update_avg_response_time(purchase_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)