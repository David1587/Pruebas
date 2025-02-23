from django.urls import path
from .views import (
    get_vulnerabilities, fix_vulnerability, get_unfixed_vulnerabilities, get_summary_by_severity, fetch_nist_vulnerabilities
)

urlpatterns = [
    path('vulnerabilities/', get_vulnerabilities, name='all_vulnerabilities'),
    path('vulnerabilities/fixed/', fix_vulnerability, name='fix_vulnerabilities'),
    path('vulnerabilities/unfixed/', get_unfixed_vulnerabilities, name='unfixed_vulnerabilities'),
    path('vulnerabilities/summary/', get_summary_by_severity, name='summary_by_severity'),
    path('vulnerabilities/fetch_nist/', fetch_nist_vulnerabilities, name='fetch_nist'),
]
