from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect

from web.models import Game, Basket
from web.forms import GameForm


class GameListView(ListView):
    template_name = 'web/home_page.html'
    model = Game
    context_object_name = 'games'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class GameDetailView(DetailView):
    pass


class GameCreateView(CreateView):
    template_name = 'web/game_add.html'
    form_class = GameForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home_page')


class GameDeleteView(DeleteView):
    pass


class GameUpdateView(UpdateView):
    pass


@login_required
def basket_add(request, game_id):
    current_page = request.META.get('HTTP_REFERER')
    game = Game.objects.get(id=game_id)
    baskets = Basket.objects.filter(user=request.user, game=game)

    if not baskets.exists():
        Basket.objects.create(user=request.user, game=game)
        return HttpResponseRedirect(current_page)
    else:
        basket = baskets.first()
        basket.save()
        return HttpResponseRedirect(current_page)


@login_required
def basket_delete(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
