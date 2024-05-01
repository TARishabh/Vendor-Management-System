from rest_framework import generics
from .models import Vendor,PurchaseOrder
from .serializers import VendorPostSerializer,VendorRetrieveSerializer,PurchaseOrderCreateUpdateSerializer,PurchaseOrderDetailSerializer,PurchaseOrderUpdateSerializer
from .models import Vendor, HistoricalPerformance
from .serializers import HistoricalPerformanceSerializer
from rest_framework.response import Response

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
    
class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = HistoricalPerformanceSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        historical_performance = HistoricalPerformance.objects.filter(vendor=instance)
        serializer = self.get_serializer(historical_performance, many=True)
        return Response(serializer.data)