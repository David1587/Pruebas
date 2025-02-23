from django.db import models

class Vulnerability(models.Model):
    SEVERITY_CHOICES = [
        ('CRITICAL', 'Critical'),
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    cve_id = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    published_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    is_fixed = models.BooleanField(default=False)

    def __str__(self):
        return self.cve_id
