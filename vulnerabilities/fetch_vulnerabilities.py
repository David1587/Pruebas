import requests
from datetime import datetime
from .models import Vulnerability

def fetch_vulnerabilities():
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    params = {"resultsPerPage": 20}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Error al consumir la API: {response.text}")

    data = response.json()
    return data.get("result", {}).get("CVE_Items", [])

def update_vulnerabilities():
    vulnerabilities = fetch_vulnerabilities()
    for item in vulnerabilities:
        cve_id = item["cve"]["CVE_data_meta"]["ID"]
        
        # Extraer la descripción, asegurando que no sea None
        description_data = item["cve"].get("description", {}).get("description_data", [])
        description = description_data[0]["value"] if description_data else "No description available"
        
        # Extraer severidad de la sección de métricas (si está disponible)
        severity = "UNKNOWN"
        impact = item.get("impact", {}).get("baseMetricV3", {}).get("cvssV3", {})
        if impact:
            severity = impact.get("baseSeverity", "UNKNOWN").upper()  # Convertimos a mayúsculas para coincidir con `SEVERITY_CHOICES`

        # Convertir fechas
        published_date = datetime.strptime(item["publishedDate"], "%Y-%m-%dT%H:%MZ")
        last_modified_date = datetime.strptime(item["lastModifiedDate"], "%Y-%m-%dT%H:%MZ")

        # Guardar en la base de datos
        Vulnerability.objects.update_or_create(
            cve_id=cve_id,
            defaults={
                "description": description,
                "severity": severity if severity in dict(Vulnerability.SEVERITY_CHOICES) else "UNKNOWN",
                "published_date": published_date,
                "last_modified_date": last_modified_date,
            }
        )
