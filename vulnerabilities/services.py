import requests
from datetime import datetime
from .models import Vulnerability

def fetch_vulnerabilities():
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    params = {
        "resultsPerPage": 20,
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error al consumir la API: {response.text}")

    data = response.json()
    return data.get("result", {}).get("CVE_Items", [])

def update_vulnerabilities():
    vulnerabilities = fetch_vulnerabilities()
    
    for item in vulnerabilities:
        cve_id = item["cve"]["CVE_data_meta"]["ID"]
        
        # Extraer la descripción de la vulnerabilidad
        description_data = item["cve"].get("description", {}).get("description_data", [])
        description = description_data[0]["value"] if description_data else "No description available"
        
        # Intentar extraer la severidad desde la métrica de la CVE (ajustar según formato real)
        severity = "MEDIUM"  # Valor por defecto
        impact = item.get("impact", {}).get("baseMetricV3", {})
        if impact:
            severity = impact.get("cvssV3", {}).get("baseSeverity", "MEDIUM")
        
        # Convertir fechas con manejo de errores en caso de formatos inesperados
        try:
            published_date = datetime.strptime(item["publishedDate"], "%Y-%m-%dT%H:%MZ")
        except ValueError:
            published_date = None  # En caso de error, almacenar `None` en lugar de fallar

        try:
            last_modified_date = datetime.strptime(item["lastModifiedDate"], "%Y-%m-%dT%H:%MZ")
        except ValueError:
            last_modified_date = None
        
        # Guardar en la base de datos
        Vulnerability.objects.update_or_create(
            cve_id=cve_id,
            defaults={
                "description": description,
                "severity": severity,
                "published_date": published_date,
                "last_modified_date": last_modified_date,
            }
        )
