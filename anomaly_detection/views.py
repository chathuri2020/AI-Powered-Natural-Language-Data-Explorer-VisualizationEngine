from django.shortcuts import render
from .anomaly_detector import detect_anomalies
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

def anomaly_view(request):
    anomalies, chart_base64 = detect_anomalies()
    context = {
        'anomalies': anomalies.to_dict(orient='records'),
        'chart_base64': chart_base64, 
        'name':"Chathuri"
    }
  
    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))


   