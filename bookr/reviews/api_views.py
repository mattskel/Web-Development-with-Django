from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Book, Contributor, Review
from .serializers import BookSerializer, ContributorSerializer, ReviewSerializer

@api_view()
def first_api_view(request):
    num_books = Book.objects.count()
    return Response({"num_books": num_books})

@api_view()
def all_books(request):
    books = Book.objects.all()
    book_serializer = BookSerializer(books, many=True)
    return Response(book_serializer.data)

class AllBooks(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ContributorView(generics.ListAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.order_by('-date_created')
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = []