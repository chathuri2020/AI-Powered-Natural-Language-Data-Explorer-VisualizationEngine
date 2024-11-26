from django.shortcuts import render
from .anomaly_detector import detect_anomalies
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def anomaly_view(request):
    selected_option = "transaction"
    if request.method == 'POST':
        data = json.loads(request.body)
        #message = request.POST.get('message')
        message ="here is the massage"
        #selected_option = data.get('selected_option')
   # anomalies = detect_anomalies(message)
    context = {
        #'anomalies': anomalies.to_dict(orient='records'),
        'anomalies':"massage is here",
        'name':"Chathuri"
    }

    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
def update_table_selection(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse the JSON body
        selected_option = data.get('selected_option')  # Retrieve the selected option
        anomalies = detect_anomalies(selected_option)
        context = {
            'anomalies': anomalies.to_dict(orient='records'),
            'name':"Chathuri",
        }
        html_template = loader.get_template('home/dashboard.html')
        return HttpResponse(html_template.render(context, request))

    