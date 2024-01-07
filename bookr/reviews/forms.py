from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Publisher
from .models import Review
from .models import Book

SEARCH_CHOICES = (
    ("title", "Title"),
    ("contributor", "Contributor")
)

class InstanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        if kwargs.get("instance"):
            button_title = "Save"            
        else:
            button_title = "Create"

        self.helper.add_input(Submit("", button_title))

class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False, choices=SEARCH_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.add_input(Submit("", "Search"))

class PublisherForm(InstanceForm):
    class Meta:
        model = Publisher
        # fields = ("name", "website", "email")
        fields = "__all__"

class ReviewForm(InstanceForm):
    class Meta:
        model = Review
        exclude = ["date_edited", "book"]

    rating = forms.IntegerField(max_value=5, min_value=0)    

class BookMediaForm(InstanceForm):
    class Meta:
        model = Book
        fields = ['cover', 'sample']