"""steam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.GameListView.as_view(), name='home_page'),
    path('add_game/', login_required(views.GameCreateView.as_view()), name='add_game'),
    path('<slug:slug>/<int:id>', views.GameDetailView.as_view(), name='detail_game'),
    path('<slug:slug>/<int:id>/delete', login_required(views.GameDeleteView.as_view()), name='update_game'),
    path('<slug:slug>/<int:id>/edit', login_required(views.GameUpdateView.as_view()), name='delete_game'),
    path('<slug:slug>/<int:game_id>/comment_delete/<int:id>/', login_required(views.CommentDeleteView.as_view()),
         name='delete_comment'),
    path('<slug:slug>/<int:game_id>/comment_edit/<int:id>/', login_required(views.CommentUpdateView.as_view()),
         name='update_comment'),
    path('basket_add/<int:game_id>/', views.basket_add, name='basket_add'),
    path('basket_delete/<int:id>/', views.basket_delete, name='basket_delete'),
]
