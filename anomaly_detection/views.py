from django.shortcuts import render
from anomaly_detection.management.commands import Command

def anomaly_detection_view(request):
    anomalies = Command()
    context = {
        "anomalies": anomalies,
        "error": anomalies.get("error", None)
    }
    return render(request, 'transactions/anomalies.html', context)
