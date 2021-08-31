from django.shortcuts import render
from .contrapunctus import Contrapunctus
from django.core import serializers
from django.http import JsonResponse

def counterpoint(request):
    result = Contrapunctus(request.POST['key'])
    melody = request.POST['melody'].split(',')
    melody = list(map(int, melody))
    return JsonResponse({'counterpoint':result.generate(melody, int(request.POST['vertical']))})


# Create your views here.
