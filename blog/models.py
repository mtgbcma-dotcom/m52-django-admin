from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField("título", max_length=200)
    content = models.TextField("conteúdo")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="autor",
    )
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)
    published_at = models.DateTimeField("publicado em", null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return self.title

    def publish(self):
        self.published_at = timezone.now()
        self.save(update_fields=["published_at", "updated_at"])
