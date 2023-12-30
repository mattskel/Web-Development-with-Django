from io import BytesIO
from PIL import Image
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.core.files.images import ImageFile

from .models import Book, Contributor, Publisher, Review
from .utils import average_rating
from .forms import SearchForm, PublisherForm, ReviewForm, BookMediaForm

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

def publisher_edit(request, pk=None):
    if pk is not None:
        # Do something here
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == "POST":
        # Instantiate the form
        # The form is bound if it is called with some data to be used for validation
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, "Publisher \"{}\" was created.".format(updated_publisher))
            else: 
                messages.success(request, "Publisher \"{}\" was updated.".format(updated_publisher))

            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(request, "reviews/instance-form.html", {
        "form": form, 
        "instance": publisher,
        "model_type": "Publisher"
    })

def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)
    if review_pk is None:
        review = None
    else:
        review = get_object_or_404(Review, pk=review_pk, book_id=book_pk)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(False)
            updated_review.book = book

            if review is None:
                messages.success(request, "Review \"{}\" was created.".format(book))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, "Review \"{}\" was updated.".format(book)) 

            updated_review.save()
            return redirect("book_detail", book_pk)

    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/instance-form.html", {
        "form": form,
        "instance": review,
        "model_type": "Review",

    })

def book_media(request, pk):
    instance = get_object_or_404(Book, pk=pk)
    print(instance.isbn)
    if request.method == 'POST':
        form = BookMediaForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(False)
            if form.cleaned_data['cover']:
                image = Image.open(form.cleaned_data['cover'])
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(fp=image_data, format = form.cleaned_data['cover'].image.format)
                image_file = ImageFile(image_data)
                instance.cover.save(form.cleaned_data['cover'].name, image_file)

            instance.save()
            messages.success(request, "Book \"{}\" was successfully updated.".format(instance))
            return redirect("book_detail", pk)

    else:
        form = BookMediaForm(instance=instance)

    print('instance', instance)
    return render(request, 'reviews/instance-form.html', {
        "form": form, 
        "model_type": 'Book',
        "instance": instance,
        "is_file_upload": True})