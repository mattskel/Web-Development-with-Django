import datetime

from django.db.models import Count
from reviews.models import Review

def get_books_read_by_month(username):
    """Get books read by the user on a per month basis"""
    # current_year = datetime.datetime.now().year
    current_year = 2023
    books = (
        Review.objects
            .filter(creator__username__contains=username, date_created__year=current_year)
            .values('date_created__month')
            .annotate(book_count=Count('book__title'))) # Count groups on title prop and adds to object
    return books

def get_books_read(username):
    books = (
        Review.objects
        .filter(creator__username__contains=username)
        .all())

    return [{'title': book_read.book.title} for book_read in books]