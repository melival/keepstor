from django.shortcuts import render
from django.http import HttpResponse as response
from . import keepstor

# Create your views here.
html_head = "<!DOCTYPE html><head><title>TableView</title></head>"
html_open = "<html>"
html_close = "</html>"
def show(request):
    result = html_head + html_open
    result += keepstor.get_http_result_table()
    result += html_close
    return response(result)