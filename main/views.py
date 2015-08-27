from pprint import pprint

from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Api
from lootTracker.models import Character


# Create your views here.
PAGE_TITLE = 'Phearless, Naughty and Ugly Scoundrels'


def index(request):
	user_name = request.user.username
	return render(request, 'main/home.html', {
		'page_title': PAGE_TITLE,
		'user_name': user_name,
		'user_logged_in': request.user.is_authenticated()
	})


def logout(request):
	django_logout(request)
	return redirect('index')


def login(request):
	if request.method != 'POST':
		view = render(request, 'main/login.html', {
			'page_title': PAGE_TITLE
		})
	else:
		# Handle the form.
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is None:
			request.session['failed_logins'] = request.session.get('failed_logins', 1) + 1
			view = render(request, 'main/login.html', {
				'page_title': PAGE_TITLE,
				'failed': request.session['failed_logins']
			})
		else:
			django_login(request, user)
			view = redirect('/')
	return view


def signup(request):
	if request.method != 'POST':
		view = render(request, 'main/login.html', {
			'page_title': PAGE_TITLE
		})
	else:
		# @todo Server-side input validation. Client-side doesn't cut it.
		user = User.objects.create_user(request.POST['username'], '', request.POST['password'])
		api = Api(user=user, key=request.POST['key'], verification_code=request.POST['vcode'])
		user.save()
		api.save()
		user = authenticate(username=request.POST['username'], password=request.POST['password'])

		# Now associate the characters to this account.
		for char_id in request.session['characters']:
			character = Character.objects.get(eve_id=char_id)

			if character is not None:
				character.user = user
				character.save()
			else:
				pprint('Character' + char_id + ' does not exist.')

		django_login(request, user)
		view = redirect('/')  # @todo This should redirect to character picking.

	return view
