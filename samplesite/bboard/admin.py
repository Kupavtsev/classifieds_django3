from django.contrib import admin

# Register your models here.
from .models        import Bb, Rubric

class BbAdmin(admin.ModelAdmin) :
    list_display = (
                'title',
                'content',
                'price',
                'published',
                'changed',
                'rubric'
                )
    list_display_links = (
                'title', 
                'content', 
                'changed'
                )
    search_fields = (
                'title', 
                'content', 
                'changed' 
                )

admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)