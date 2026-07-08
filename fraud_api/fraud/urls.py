from django.urls import path
from .views import (
    detect_fraud,
    realtime_fraud_check,
    fraud_transactions,
    dashboard_summary,
    export_fraud_csv
)

urlpatterns = [
    path('detect/', detect_fraud),
    path('realtime-check/', realtime_fraud_check),
    path('fraud-transactions/', fraud_transactions),
    path('dashboard-summary/', dashboard_summary),
    path('export-csv/', export_fraud_csv),
]