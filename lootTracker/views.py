from .models import Fleet, Item, Drop

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from pprint import pprint


# Create your views here.


@login_required
def index(request):
    drops = Drop.objects.filter(fleet=Fleet(pk=1))  # @todo Use real fleet.
    fleet_total = 0

    for drop in drops:
        drop.total = drop.item_current_value * drop.quantity
        fleet_total += drop.total

    return render(request, 'lootTracker/main.html', {
        'page_title': 'Loot Tracker',
        'fleets': Fleet.objects.filter(finalized=False).all(),
        'items': Item.objects.all(),
        'drops': drops,
        'fleet_total': fleet_total
    })
