from django.db import models

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=50, unique=True)  # ID único del CVE
    description = models.TextField()
    severity = models.CharField(max_length=20)  
    fixed = models.BooleanField(default=False)  # Indica si está fixeada
