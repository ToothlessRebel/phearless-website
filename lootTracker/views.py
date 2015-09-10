from .models import Fleet, Item, Character, FleetType, FleetRestriction

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from pprint import pprint


# Create your views here.


@login_required
def index(request):
    return render(request, 'lootTracker/main.html', {
        'page_title': 'Loot Tracker',
        'items': Item.objects.all(),
        'characters': Character.objects.all(),
        'types': FleetType.objects.all(),
        'restrictions': FleetRestriction.objects.all()
    })
