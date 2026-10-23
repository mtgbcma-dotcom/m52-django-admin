from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from .models import Post


class PostView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello World", content_type="text/plain; charset=utf-8")


def post_list(request):
    posts = Post.objects.filter(published_at__lte=timezone.now()).select_related("author")
    return render(request, "blog/post_list.html", {"posts": posts})
