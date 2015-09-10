from pprint import pprint

from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .models import Api
from lootTracker.models import Character


# Create your views here.
PAGE_TITLE = 'Phearless, Naughty and Ugly Scoundrels'


def index(request):
    return render(request, 'main/home.html', {
        'page_title': PAGE_TITLE
    })


def logout(request):
    django_logout(request)
    return redirect('index')


def login(request):
    request.session['next'] = request.GET['next'] if 'next' in request.GET else request.session.get('next', '/')
    if request.method != 'POST':
        view = render(request, 'main/login.html', {
            'page_title': PAGE_TITLE,
            'failed': request.session.get('failed_logins', 0)
        })
    else:
        # Handle the form.
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            request.session['failed_logins'] = request.session.get('failed_logins', 0) + 1
            view = render(request, 'main/login.html', {
                'page_title': PAGE_TITLE,
                'failed': request.session.get('failed_logins', 0)
            })
        else:
            django_login(request, user)
            view = redirect(request.session.get('next', '/'))
            request.session.delete('next')

    return view


def signup(request):
    request.session['next'] = request.GET['next'] if 'next' in request.GET else request.session.get('next', '/')
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
        view = redirect('/user/characters')

    return view


@login_required
def pick_characters(request):
    return render(request, 'main/characters.html', {
        'page_title': PAGE_TITLE,
        'characters': request.user.character_set.all()
    })


@login_required
def set_character(request, character_id):
    character = Character.objects.filter(pk=character_id).get()
    request.user.api.default_character = character
    request.user.save()
    view = redirect(request.session.get('next', '/'))
    request.session.delete('next')

    return view
