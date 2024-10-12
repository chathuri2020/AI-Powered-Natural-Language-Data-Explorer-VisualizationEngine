# views.py
from django.http import JsonResponse
from django.shortcuts import render




def chat_assistant(request):
    obj = [
    {"order_id": 101, "customer_name": "Alice", "product": "Laptop", "quantity": 2, "price": 1200},
    {"order_id": 102, "customer_name": "Bob", "product": "Phone", "quantity": 1, "price": 800},
    {"order_id": 103, "customer_name": "Charlie", "product": "Tablet", "quantity": 3, "price": 600},
]
    template_name = 'chatbot/chatbot.html'
    context = {'obj': obj}
    return render(request, template_name, context)


def updateView(request, f_oid):
   # obj = Orders.objects.get(oid=f_oid)
    #form = OrderForm(instance=obj)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('show_url')
    template_name = 'crudapp/order.html'
    context = {'form': form}
    return render(request, template_name, context)