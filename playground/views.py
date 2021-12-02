from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from store.models import Product, Order

# Create your views here.
def say_hello(request):
    query_set = Order.objects.select_related('customer').order_by('-placed_at')[:5]
    return render(request, 'hello.html',{'orders': list(query_set)})