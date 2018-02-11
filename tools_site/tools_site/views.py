from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import generic
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import json
import os
import os.path as path

def cpu_data(request):
    MAX = 60
    PATH = "tools_site"
    SUFFIX = ".log"
    def get_cpu_log_files():
        log_files = [f for f in os.listdir(PATH) if f.endswith(SUFFIX)]
        return log_files
    def get_cpu_data(filename):
        fullname = path.join(PATH, filename)
        lines = []
        with open(fullname) as stream:
            for line in stream:
                line = line.strip('\r\n')
                lines.append(line)
        result = lines[-MAX:]
        for i in range(len(result), MAX, 1):
            result.insert(0, 0)
        return result

    log_files = get_cpu_log_files()
    log_files.sort()
    result = {}
    for filename in log_files:
        key = filename[:filename.index(SUFFIX)]
        data = get_cpu_data(filename)
        result[key] = data
    return HttpResponse(json.dumps(result))

