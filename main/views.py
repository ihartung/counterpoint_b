from django.shortcuts import render
from .contrapunctus import Contrapunctus
from django.core import serializers
from django.http import JsonResponse

def counterpoint(request):
    result = Contrapunctus(request.POST['key'])
    melody = request.POST['melody'].split(',')
    if len(melody) > 50:
        return JsonResponse({'message':'melody too long, must be 50 notes or less'})
    melody = list(map(int, melody))
    return JsonResponse({'counterpoint':result.generate(melody, int(request.POST['vertical']))})


# Create your views here.
