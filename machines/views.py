# oee_calculation/views.py
from rest_framework import viewsets, status,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Machine, ProductionLog
from .serializers import MachineSerializer, ProductionLogSerializer
from django.db.models import Sum, F, ExpressionWrapper, FloatField

def calculate_oee(production_logs):
    total_duration = production_logs.aggregate(total_duration=Sum('duration'))['total_duration']
    total_output = production_logs.count()
    good_products = production_logs.filter(duration=5).count()
    availability = (24 - total_duration) / 24 * 100
    performance = (5 * total_output) / total_duration * 100
    quality = (good_products / total_output) * 100
    oee = availability * performance * quality / 10000
    return round(oee, 2)

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductionLogViewSet(viewsets.ModelViewSet):
    queryset = ProductionLog.objects.all()
    serializer_class = ProductionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def oee(self, request):
        machines = Machine.objects.all()
        oee_data = []
        for machine in machines:
            production_logs = ProductionLog.objects.filter(machine=machine)
            oee = calculate_oee(production_logs)
            oee_data.append({
                'machine': machine.machine_name,
                'oee': oee
            })
        return Response(oee_data)

    @action(detail=False, methods=['get'])
    def id(self, request):
        machine_id = request.query_params.get('machine_id')
        if not machine_id:
            return Response({'error': 'Machine ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        machine = Machine.objects.filter(id=machine_id).first()
        if not machine:
            return Response({'error': 'Machine not found'}, status=status.HTTP_404_NOT_FOUND)
        production_logs = ProductionLog.objects.filter(machine=machine)
        oee = calculate_oee(production_logs)
        return Response({'machine': machine.machine_name, 'oee': oee})

    @action(detail=False, methods=['get'])
    def date(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not start_date or not end_date:
            return Response({'error': 'Start date and end date are required'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        production_logs = ProductionLog.objects.filter(start_time__gte=start_date, end_time__lte=end_date)

        if not production_logs:
            return Response({'message': 'No production logs found for the given date range'},
                            status=status.HTTP_400_BAD_REQUEST)    

        oee = calculate_oee(production_logs)
        return Response({'start_date': start_date, 'end_date': end_date, 'oee': oee})
