from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language

#admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)
admin.site.register(Language)

class BookInline(admin.TabularInline):  
    model = Book.authors.through
    extra = 0
    readonly_fields = ('book',)
    can_delete = False

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    search_fields = ('first_name', 'last_name')
    inlines = [BookInline]
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_authors', 'display_genre')
    search_fields = ('title', 'authors__first_name', 'authors__last_name', 'genre__name')
    inlines = [BooksInstanceInline]

    def display_authors(self, obj):
        return ", ".join(author.__str__() for author in obj.authors.all())
    display_authors.short_description = 'Authors'

    def display_genre(self, obj):
        return ", ".join(genre.name for genre in obj.genre.all())
    display_genre.short_description = 'Genre'


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')  # filter sidebar for easy filtering

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


