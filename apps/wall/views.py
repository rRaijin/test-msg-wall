from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView


def logout(request):
    auth.logout(request)

    return redirect('wall:login')


def index(request):
    return render(request, 'index.html')


class Wall(TemplateView):
    template_name = 'wall/wall-msg.html'