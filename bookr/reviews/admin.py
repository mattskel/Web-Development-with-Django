from django.contrib import admin
from reviews.models import (Publisher, Contributor, Book, BookContributor, Review)


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn', 'publisher__name')
    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn13', 'has_isbn', 'get_publisher')
    list_filter = ('publisher', 'publication_date')

    @admin.display(boolean=True, description='Has ISBN')
    def has_isbn(self, obj):
        return bool(obj.isbn)

    def get_publisher(sef, obj):
        return obj.publisher.name


class ReviewAdmin(admin.ModelAdmin):
    exclude = ('date_edited',)
    fieldsets = (
        (None, {"fields": ("creator", "book")}),
        ("Review content", {"fields": ("content", "rating")}),
    )


def initialled_name(obj):
    initials = ''.join([name[0] for name in obj.first_names.split(' ')])
    return "{}, {}".format(obj.last_names, initials)


class ContributorAdmin(admin.ModelAdmin):
    list_display = ("last_names", "first_names")
    search_fields = ('first_names', 'last_names__startswith')
    list_filter = ('last_names', )


# Register your models here.
admin.site.register(Publisher)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review, ReviewAdmin)
