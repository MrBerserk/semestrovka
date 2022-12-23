from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from web.models import Basket

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home_page'))
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {
        'form': form
    })


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {
        'form': form
    })


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserProfileForm(instance=user)
    baskets = Basket.objects.filter(user=user)
    total_sum = sum(basket.sum() for basket in baskets)
    return render(request, 'users/profile.html', {
        'form': form,
        'baskets': Basket.objects.filter(user=user),
        'total_sum': total_sum,
    })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home_page'))
