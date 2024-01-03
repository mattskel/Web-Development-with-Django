from django.contrib import admin
from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.index),
    path('books', views.book_list, name='book_list'),
    path('books/<int:pk>', views.book_detail, name='book_detail'),
    path('book-search/', views.book_search, name='book_search'),
    path('publishers/<int:pk>', views.publisher_edit, name="publisher_edit"),
    path('publishers/new', views.publisher_edit, name="publisher_create"),
    path('books/<book_pk>/reviews/new', views.review_edit, name="review_create"),
    path('books/<book_pk>/reviews/<review_pk>', views.review_edit, name="review_edit"),
    path('books/<pk>/media/', views.book_media, name="media"),
    path('api/first_api_view/', api_views.first_api_view),
    path('api/all_books/', api_views.AllBooks.as_view(), name='all_books'),
    path('api/contributors/', api_views.ContributorView.as_view(), name='contributors')
]
