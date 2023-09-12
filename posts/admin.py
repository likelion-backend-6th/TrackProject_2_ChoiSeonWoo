from datetime import datetime

from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug", "author", "status", "publish", "tag_list"]
    list_filter = ["publish", "created_at", "updated_at"]
    search_fields = ["title", "author", "body"]
    raw_id_fields = ["author"]
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        new_publish_date = form.data.get("publish_0")
        new_publish_time = form.data.get("publish_1")
        new_publish_microsecond = datetime.now().microsecond
        datetime_str = (
            f"{new_publish_date} {new_publish_time}.{new_publish_microsecond:06d}"
        )
        new_publish = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")

        if change:
            existing_publish_data = Post.objects.get(id=obj.id).publish
            if existing_publish_data.strftime(
                "%Y-%m-%d %H:%M:%S"
            ) == obj.publish.strftime("%Y-%m-%d %H:%M:%S"):
                obj.publish = existing_publish_data
            else:
                obj.publish = new_publish
        else:
            obj.publish = new_publish

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
