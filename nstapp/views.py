from django.http import request
from django.shortcuts import render


# Create your views here.
def test():
    return render(request, 'test.html')
