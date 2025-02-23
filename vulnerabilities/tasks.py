from celery import shared_task
from .fetch_vulnerabilities import update_vulnerabilities  # Import local

@shared_task
def update_vulns_task():
    update_vulnerabilities()
    return "✔ Vulnerabilidades actualizadas"
