from django.shortcuts import render
from django.http import HttpResponse as response

# Create your views here.

def show(request):
    return response("Heellooo ya!")