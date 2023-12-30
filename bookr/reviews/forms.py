from django import forms

from .models import Publisher
from .models import Review
from .models import Book

SEARCH_CHOICES = (
    ("title", "Title"),
    ("contributor", "Contributor")
)


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False, choices=SEARCH_CHOICES)

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        # fields = ("name", "website", "email")
        fields = "__all__"

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["date_edited", "book"]

    rating = forms.IntegerField(max_value=5, min_value=0)    

class BookMediaForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['cover', 'sample']