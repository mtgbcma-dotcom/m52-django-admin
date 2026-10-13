from django.conf import settings
from django.db import models


class Post(models.Model):
    titulo = models.CharField("título", max_length=200)
    texto = models.TextField("texto")
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="autor",
    )
    criado_em = models.DateTimeField("criado em", auto_now_add=True)
    publicado = models.BooleanField("publicado", default=False)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return self.titulo