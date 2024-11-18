from django.contrib import admin

from .models import User, Post

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "password", "date_joined")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "post_author", "post_date", "post_text")
# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
