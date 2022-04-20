from django.contrib import admin
from .models import Post, BlogComments
# Register your models here.
admin.site.register(BlogComments)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('tiny.js',)
