from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "publicado", "criado_em")
    list_filter = ("publicado", "autor")
    search_fields = ("titulo", "texto")
    date_hierarchy = "criado_em"
    readonly_fields = ("criado_em",)