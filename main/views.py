from django.shortcuts import render
from musicTools.contrapunctus import Contrapunctus

def counterpoint(request):
    result = Contrapunctus(request.POST['key'])
    return result.generate(request.POST['melody'], request.POST['vertical'])


# Create your views here.
