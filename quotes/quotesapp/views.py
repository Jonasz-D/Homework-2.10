from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Author, Quote, Tag
from .forms import AuthorForm, QuoteForm, UserRegisterForm, TagForm
from django.core.paginator import Paginator
import requests
from bs4 import BeautifulSoup

from django.views.generic import TemplateView, ListView

def home(request):
    quotes = Quote.objects.all()
    return render(request, 'quotesapp/home.html', {'quotes': quotes})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'quotesapp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'quotesapp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'quotesapp/add_author.html', {'form': form})

@login_required
def add_quote(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            return redirect('home')
        else:
            
            return render(request, 'quotesapp/add_quote.html', {'tags':tags, 'form': form})
    else:
        return render(request, 'quotesapp/add_quote.html', {"tags": tags, 'form': QuoteForm()})

def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_quote')
    else:
        form = TagForm()
    return render(request, 'quotesapp/add_tag.html', {'form': form})

def quote_detail(request, quote_id):
    quotes = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quotesapp/quote_detail.html', {"quotes": quotes})