from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Book, Contributor
from .utils import average_rating
from .forms import SearchForm 

def index(request):
    return render(request, "base.html")


def book_search(request):
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        else:
            contributors = Contributor.objects.filter(Q(first_names__icontains=search) | Q(last_names__icontains=search))
            print("contributors", contributors)
            for contributor in contributors:
                for book in contributor.book_set.all():
                    books.add(book)
    
    search_text = request.GET.get("search", "")
    return render(request, "reviews/search-results.html", {"search_text": search_text, "books": books, "form": form})


def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({'book': book,
                          'book_rating': book_rating,
                          'number_of_reviews': number_of_reviews})

    context = {'book_list': book_list}
    return render(request, 'reviews/book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    if reviews:
        overall_rating = average_rating([review.rating for review in reviews])
    else:
        overall_rating = None

    context = {'book': book,
               'reviews': reviews,
               'overall_rating': overall_rating}
    return render(request, 'reviews/book_detail.html', context)
