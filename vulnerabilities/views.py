from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Vulnerability
from .serializers import VulnerabilitySerializer
import requests

# 1. Obtener todas las vulnerabilidades
@api_view(['GET'])
def get_vulnerabilities(request):
    vulnerabilities = Vulnerability.objects.all()
    serializer = VulnerabilitySerializer(vulnerabilities, many=True)
    return Response(serializer.data)

# 2. Marcar vulnerabilidad como fixeada
@api_view(['POST'])
def fix_vulnerability(request):
    cve_ids = request.data.get('cve_ids', [])  # Lista de CVE a fixear
    Vulnerability.objects.filter(cve_id__in=cve_ids).update(fixed=True)
    return Response({"message": "Vulnerabilidades marcadas como fixeadas"}, status=status.HTTP_200_OK)

# 3. Obtener vulnerabilidades no fixeadas
@api_view(['GET'])
def get_unfixed_vulnerabilities(request):
    vulnerabilities = Vulnerability.objects.filter(fixed=False)
    serializer = VulnerabilitySerializer(vulnerabilities, many=True)
    return Response(serializer.data)

# 4. Obtener resumen por severidad
from django.db import models

@api_view(['GET'])
def get_summary_by_severity(request):
    summary = Vulnerability.objects.filter(fixed=False).values('severity').annotate(count=models.Count('severity'))
    return Response(summary)

    return Response(summary)

# 5. Cargar vulnerabilidades desde la API del NIST
@api_view(['POST'])
def fetch_nist_vulnerabilities(request):
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json().get("result", {}).get("CVE_Items", [])
        
        for item in data:
            cve_id = item["cve"]["CVE_data_meta"]["ID"]
            description = item["cve"]["description"]["description_data"][0]["value"]
            severity = item.get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {}).get("baseSeverity", "Unknown")

            Vulnerability.objects.update_or_create(
                cve_id=cve_id,
                defaults={"description": description, "severity": severity}
            )

        return Response({"message": "Vulnerabilidades cargadas desde NIST"}, status=status.HTTP_201_CREATED)
    
    return Response({"error": "No se pudo obtener datos del NIST"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
