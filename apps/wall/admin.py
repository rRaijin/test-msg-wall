from django.contrib import admin
from .models import *


class MessageAdmin(admin.ModelAdmin):
    list_display = ["author", "posted", "edited"]
    search_fields = ["author", "posted"]

admin.site.register(Message, MessageAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "message", "parent", "posted", "edited"]
    search_fields = ["author", "message", "posted"]

admin.site.register(Comment, CommentAdmin)