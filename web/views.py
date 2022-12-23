from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required

from web.models import Game, Comment, Basket
from web.forms import GameForm, CommentForm


class GameListView(ListView):
    template_name = 'web/home_page.html'
    model = Game
    context_object_name = 'games'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class GameDetailView(FormMixin, DetailView):
    template_name = 'web/'
    form_class = GameForm
    model = Game
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_game', args=(self.kwargs['slug'], self.kwargs['id']))


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
    template_name = 'web/game_delete.html'
    model = Game
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('home_page')


class GameUpdateView(UpdateView):
    template_name = 'web/game_edit.html'
    model = Game
    form_class = GameForm
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_game', args=(self.object.slug, self.object.id))


class CommentUpdateView(UpdateView):
    template_name = 'web/comment_edit.html'
    model = Comment
    form_class = CommentForm
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.text, allow_unicode=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_game', args=(self.kwargs['slug'], self.kwargs['game_id']))

    def get_context_data(self, **kwargs):
        return {
            **super(CommentUpdateView, self).get_context_data(**kwargs),
            'slug': self.kwargs['slug'],
            'game_id': self.kwargs['game_id']
        }


class CommentDeleteView(DeleteView):
    model = Comment
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('detail_game', args=(self.object.slug, self.object.id))

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
