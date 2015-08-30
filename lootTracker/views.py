from .models import Fleet

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from pprint import pprint


# Create your views here.


@login_required
def index(request):
    fleets = Fleet.objects.filter(finalized=False).all()
    return render(request, 'main.html', {
        'page_title': 'Loot Tracker',
        'fleets': fleets
    })
