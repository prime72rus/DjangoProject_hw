from django.contrib import admin
from blog.models import Post


@admin.register(Post)
class PastAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at", "is_public", "view_counter")
    search_fields = ("title", "content")
    list_filter = ("is_public", "view_counter", "created_at")