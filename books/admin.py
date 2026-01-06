from django.contrib import admin
from .models import Book, Review, Category

# Update admin site titles
admin.site.site_header = 'Books Store Admin'
admin.site.site_title = 'Books Store'
admin.site.index_title = 'Books Admin'

class BookAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    list_filter = ['category']

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']

admin.site.register(Book, BookAdmin)
admin.site.register(Review)
admin.site.register(Category, CategoryAdmin)