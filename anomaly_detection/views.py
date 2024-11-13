# views.py
from django.shortcuts import render
from django.http import JsonResponse
from anomaly_detection.management.commands.detect_anomalies import Command

def show_anomalies(request):
    # Instantiate the command class and call the `detect_anomalies` method
    anomalies_detector = Command()
    anomalies = anomalies_detector.detect_anomalies()

    # Optionally, you can render this in a template or return as JSON
    return render(request, 'anomalies.html', {'anomalies': anomalies})
