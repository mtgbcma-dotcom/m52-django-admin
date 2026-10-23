from django.contrib import admin
from django.utils import timezone

from .models import Post


class PublicationStatusFilter(admin.SimpleListFilter):
    title = "publicação"
    parameter_name = "publication_status"

    def lookups(self, request, model_admin):
        return (("published", "Publicados"), ("unpublished", "Não publicados"))

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == "published":
            return queryset.filter(published_at__lte=now)
        if self.value() == "unpublished":
            return queryset.exclude(published_at__lte=now)
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "created_at", "published_at")
    list_filter = (PublicationStatusFilter, "author", "published_at")
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("author",)

    @admin.display(boolean=True, description="Publicado", ordering="published_at")
    def is_published(self, obj):
        return obj.published_at is not None and obj.published_at <= timezone.now()

    @admin.action(description="Publicar posts selecionados")
    def publish_posts(self, request, queryset):
        for post in queryset:
            post.publish()

    actions = ["publish_posts"]
