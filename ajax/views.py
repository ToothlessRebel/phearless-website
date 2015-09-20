from pprint import pprint
from lootTracker.models import Item, Drop, Fleet, FleetType, FleetRestriction

from xml.etree.ElementTree import fromstring
from xml.parsers.expat import ExpatError

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import render

from collections import namedtuple
import requests
import json

from lootTracker.models import Alliance, Character, Corporation

struct = namedtuple("SIZE_SUFFIX", 'ALLIANCE CHARACTER CORPORATION ITEM')
SIZE_SUFFIXES = struct(ALLIANCE='_128.png', CHARACTER='_512.jpg', CORPORATION='_256.png', ITEM='_64.png')

IMG_SERVER_URL = 'https://image.eveonline.com/'


# Create your views here.


def check_username(request, username):
    response = {'result': False}
    if User.objects.filter(username=username).exists():
        response['result'] = True
    return HttpResponse(json.dumps(response), content_type="application/json")


def parse_api(request):
    api_response = request.POST['api']
    tree = None
    response = {'result': 'success'}

    try:
        tree = fromstring(api_response)
    except ExpatError:
        # pprint('Failed to parse.')
        pass

    characters = []
    character_ids = []
    alliances = []
    corporations = []

    if tree is not None:
        group = tree.find('result/key/rowset')

        # Grab all the characters
        for row in group.getiterator('row'):
            char_id = row.attrib['characterID']
            character_ids.append(char_id)
            characters.append({
                'name': row.attrib['characterName'],
                'id': char_id,
                'corporation': row.attrib['corporationID'],
            })

        # Store the characters in the session to associate them with the user
        request.session['characters'] = character_ids

        # Grab all the corporations
        for row in group.getiterator('row'):
            corporations.append({
                'name': row.attrib['corporationName'],
                'id': row.attrib['corporationID'],
                'alliance': row.attrib['allianceID']
            })

        # Lastly, grab the alliances
        for row in group.getiterator('row'):
            alliances.append({
                'name': row.attrib['allianceName'],
                'id': row.attrib['allianceID']
            })

        # Some Ruby look-alike magic to make the lists unique
        corporations = list({value['id']: value for value in corporations}.values())
        alliances = list({value['id']: value for value in alliances}.values())

        for imported in alliances:
            if not Alliance.objects.filter(eve_id=imported['id']).exists():
                alliance = Alliance(
                    name=imported['name'],
                    eve_id=imported['id']
                )
                request = requests.get(IMG_SERVER_URL + '/Alliance/' + str(alliance.eve_id) + SIZE_SUFFIXES.ALLIANCE)
                if request.status_code == requests.codes.ok:
                    temp_img = NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break  # EOF
                        temp_img.write(block)
                    alliance.portrait.save(str(alliance.eve_id) + '_256.png', File(temp_img))
                alliance.save()

        for imported in corporations:
            if not Corporation.objects.filter(eve_id=imported['id']).exists():
                corporation = Corporation(
                    eve_id=imported['id'],
                    name=imported['name'],
                    alliance=Alliance.objects.get(eve_id=imported['alliance'])
                )
                request = requests.get(
                    IMG_SERVER_URL + '/Corporation/' + str(corporation.eve_id) + SIZE_SUFFIXES.CORPORATION)
                if request.status_code == requests.codes.ok:
                    temp_img = NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break  # EOF
                        temp_img.write(block)
                    corporation.portrait.save(str(corporation.eve_id) + '_256.png', File(temp_img))
                corporation.save()

        for imported in characters:
            if not Character.objects.filter(eve_id=imported['id']).exists():
                character = Character(
                    name=imported['name'],
                    eve_id=imported['id'],
                    corporation=Corporation.objects.get(eve_id=imported['corporation'])
                )
                request = requests.get(IMG_SERVER_URL + '/Character/' + str(character.eve_id) + SIZE_SUFFIXES.CHARACTER,
                                       stream=True)
                if request.status_code == requests.codes.ok:
                    temp_img = NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break  # EOF
                        temp_img.write(block)
                    character.portrait.save(str(character.eve_id) + '_256.jpg', File(temp_img))
                character.save()
    else:
        response['result'] = 'error'

    return HttpResponse(json.dumps(response), content_type="application/json")


def item_name_to_id(request, item_name):
    item_request = requests.get('http://www.fuzzwork.co.uk/api/typeid.php?typename=' + item_name)
    if item_request.status_code == requests.codes.ok:
        item = Item.load_from_json(item_request.content.decode('utf-8'))
        portrait_request = requests.get(IMG_SERVER_URL + '/Type/' + str(item.eve_id) + SIZE_SUFFIXES.ITEM,
                                        stream=True)
        if portrait_request.status_code == requests.codes.ok:
            temp_img = NamedTemporaryFile()
            for block in portrait_request.iter_content(1024 * 8):
                if not block:
                    break  # EOF
                temp_img.write(block)
            item.icon.save(str(item.eve_id) + SIZE_SUFFIXES.ITEM, File(temp_img))
        if item.name != 'bad item':
            item.save()
        return HttpResponse(item_request.content, content_type="application/json")


def add_drop_to_fleet(request, fleet_id, item_id, quantity):
    avg_price = 0.0
    eve_central_response = requests.get('http://api.eve-central.com/api/marketstat?typeid=' + item_id)
    tree = None

    try:
        tree = fromstring(eve_central_response.content)
    except ExpatError:
        # pprint('Failed to parse.')
        pass

    if tree is not None:
        avg_price = tree.find('marketstat/type/buy/avg').text
    else:
        # pprint('FAILED: tree is None.')
        pass

    fleet = Fleet.objects.filter(pk=fleet_id).first()
    drop = Drop(
        item=Item.objects.filter(eve_id=item_id).first(),
        quantity=quantity,
        fleet=fleet,
        item_current_value=avg_price
    ).save()

    response = {
        'result': True if drop is not None else False
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


def load_loot_table(request, fleet_id):
    fleet_total = 0

    drops = Drop.objects.filter(fleet=fleet_id).all()
    for drop in drops:
        drop.total = drop.quantity * drop.item_current_value
        fleet_total += drop.total
    corp_tax = float(fleet_total) * 0.05

    return render(request, 'lootTracker/loot_table.html', {
        'drops': drops,
        'fleet_total': float(fleet_total) - corp_tax,
        'corp_tax': corp_tax
    })


def fleet_member_icons(request, fleet_id):
    fleet = Fleet.objects.filter(pk=fleet_id).first()
    return render(request, 'lootTracker/member_icons.html', {
        'members': fleet.members.all(),
        'characters': Character.objects.exclude(id__in=fleet.members.all())
    })


def create_fleet(request):
    response = {'success': True}
    fleet_type = FleetType.objects.filter(pk=request.POST['type']).first()
    fleet = Fleet(
        name=request.POST['name'],
        type=fleet_type,
        corporation=request.user.api.default_character.corporation
    )
    member_ids = request.POST['members'].split(',')
    if request.POST['restriction']:
        fleet.restriction = FleetRestriction.objects.filter(pk=request.POST['restriction']).first()
    if fleet is not None:
        fleet.save()
        for member_id in member_ids:
            character = Character.objects.filter(pk=member_id).first()
            fleet.members.add(character)
        fleet.save()
        response['fleet_id'] = fleet.pk
    else:
        response['success'] = False
    return HttpResponse(json.dumps(response), content_type="application/json")


def load_fleets(request):
    fleets = Fleet.objects.filter(finalized=False).all()
    return render(request, 'lootTracker/fleet_list.html', {
        'fleets': fleets
    })


def finalize_fleet(request, fleet_id):
    response = {'success': True}

    fleet = Fleet.objects.filter(pk=fleet_id).first()
    fleet.finalized = True
    fleet.save()

    return HttpResponse(json.dumps(response), content_type="application/json")
