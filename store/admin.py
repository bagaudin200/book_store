from django.contrib import admin
from store.models import Book, UserBookRelation

class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']

class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'rating']

admin.site.register(Book, BookAdmin)
admin.site.register(UserBookRelation, UserBookRelationAdmin)
