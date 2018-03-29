#!/usr/bin/env python
# -*- encoding:UTF-8 -*-

from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello world ! ")