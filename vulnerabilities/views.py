from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Vulnerability
from .serializers import VulnerabilitySerializer
import requests

class VulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer

    def list(self, request):
        """GET: Listar todas las vulnerabilidades"""
        vulnerabilities = self.get_queryset()
        serializer = self.get_serializer(vulnerabilities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """GET: Listar vulnerabilidades no fixeadas"""
        vulnerabilities = self.get_queryset().filter(is_fixed=False)
        serializer = self.get_serializer(vulnerabilities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_fixed(self, request):
        """POST: Marcar vulnerabilidades como fixeadas"""
        cve_ids = request.data.get('cve_ids', [])
        if not cve_ids:
            return Response(
                {'error': 'No CVE IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated = Vulnerability.objects.filter(cve_id__in=cve_ids).update(is_fixed=True)
        return Response({'updated': updated})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """GET: Obtener resumen por severidad"""
        summary = Vulnerability.objects.values('severity')\
            .annotate(total=Count('id'), fixed=Count('id', filter=models.Q(is_fixed=True)))
        return Response(summary)
