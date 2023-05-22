from django.shortcuts import render

def find_home(request):
    return render(request, 'find/find_home.html')
