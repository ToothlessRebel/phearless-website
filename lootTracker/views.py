from .models import Fleet, Item, Drop

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from pprint import pprint


# Create your views here.


@login_required
def index(request):
    return render(request, 'lootTracker/main.html', {
        'page_title': 'Loot Tracker',
        'fleets': Fleet.objects.filter(finalized=False).all(),
        'items': Item.objects.all(),
    })
