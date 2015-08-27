from xml.etree.ElementTree import fromstring
from xml.parsers.expat import ExpatError
from django.contrib.auth.models import User
from django.http import HttpResponse
from pprint import pprint
import json

from lootTracker.models import Alliance, Character, Corporation

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
		pprint('Failed to parse.')

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
				pprint(alliance)
				alliance.save()

		for imported in corporations:
			if not Corporation.objects.filter(eve_id=imported['id']).exists():
				corporation = Corporation(
					eve_id=imported['id'],
					name=imported['name'],
					alliance=Alliance.objects.get(eve_id=imported['alliance'])
				)
				pprint(corporation)
				corporation.save()

		for imported in characters:
			if not Character.objects.filter(eve_id=imported['id']).exists():
				character = Character(
					name=imported['name'],
					eve_id=imported['id'],
					corporation=Corporation.objects.get(eve_id=imported['corporation'])
				)
				pprint(character)
				character.save()
	else:
		response['result'] = 'error'

	return HttpResponse(json.dumps(response), content_type="application/json")
