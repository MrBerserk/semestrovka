from django.shortcuts import render
from django.views.generic import ListView

from web.models import Game


class GameListView(ListView):
    template_name = 'web/home_page.html'
    model = Game
    context_object_name = 'games'
    slug_field = 'id'
    slug_url_kwarg = 'id'
