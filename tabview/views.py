from django.shortcuts import render
from django.http import HttpResponse
import os
import mimetypes

from . import keepstor

# Create your views here.
json_raw_path = "./tabview/templates/tabview/order_list.json"

def show(request):
    table_content = keepstor.get_html_result_table()

    return render(
        request,
        "tabview/index.html",
        {"table_content": table_content}
        )


def show_orderset(request):
    with open(os.path.normpath(json_raw_path)) as f:
        result = f.read()

    return render(
        request,
        "tabview/order_list.json",
        {"order_content": result}
        )

def get_orderset(request):
    json_file = os.path.normpath(json_raw_path)
    with open(json_file, "rb") as f:
        response = HttpResponse(f.read());

    file_type = mimetypes.guess_type(json_file);
    if file_type is None:
        file_type = 'application/octet-stream';

    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(json_file).st_size);
    response['Content-Disposition'] = "attachment; filename=order_list.json";

    return response;
