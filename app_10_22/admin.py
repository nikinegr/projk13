from django.contrib import admin
from .models import Post, Comment, Friendship, Profile, Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Friendship)
admin.site.register(Profile)
admin.site.register(Like)


# Register your models here.

