from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.


@login_required
def index(request):
    return HttpResponse("EVE Fleet Loot Tracker")
