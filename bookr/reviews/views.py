from django.shortcuts import render
from django.http import HttpResponse
from .models import Book


def welcome_view(request):
    return render(request, 'base.html')


def index(request):
    return render(request, "base.html")


def book_search(request):
    search_text = request.GET.get("search", "")
    return render(request, "search-results.html", {"search_text": search_text})
