from django import template

from django.contrib.auth.models import User
from reviews.models import Review

register = template.Library()

@register.inclusion_tag('book_list.html')
def book_list(username):
    # user = User.objects.get(username=username)
    # print(user.id)
    # reviews = Review.objects.filter(creator=user)
    reviews = Review.objects.filter(creator__username__contains=username)
    # print(reviews)
    # for review in reviews:
    #     print(review.book)
    # book_list = [book for review in reviews]
    # books_read = [review.book for review in reviews]
    book_list = [review.book.title for review in reviews]
    # print(books_read)
    # return {'books_read': books_read}
    return {'books_read': book_list}
