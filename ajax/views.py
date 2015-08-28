from xml.etree.ElementTree import fromstring
from xml.parsers.expat import ExpatError

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from pprint import pprint
from collections import namedtuple
import requests
import json

from lootTracker.models import Alliance, Character, Corporation

struct = namedtuple("SIZE_SUFFIX", 'ALLIANCE CHARACTER CORPORATION')
SIZE_SUFFIXES = struct(ALLIANCE='_128.png', CHARACTER='_512.jpg', CORPORATION='_256.png')

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
				request = requests.get(IMG_SERVER_URL + '/Corporation/' + str(corporation.eve_id) + SIZE_SUFFIXES.CORPORATION)
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
				request = requests.get(IMG_SERVER_URL + '/Character/' + str(character.eve_id) + SIZE_SUFFIXES.CHARACTER, stream=True)
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
