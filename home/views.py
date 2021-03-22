from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    univer = "nau"
    degr = "Bach"
    context = {'univer': univer, 'degr': degr}
    return render(request, 'home/index.html', context)

