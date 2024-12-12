from django.shortcuts import render

def index(request):
    return render(request, 'profissionais_app/index.html')