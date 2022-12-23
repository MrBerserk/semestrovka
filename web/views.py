from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse

from web.models import Game
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
        form.instance.slug = slugify(form.instance.title, allow_unicode=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home_page')


class GameDeleteView(DeleteView):
    pass


class GameUpdateView(UpdateView):
    pass
