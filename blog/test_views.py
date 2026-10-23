from django.urls import resolve, reverse
from .views import PostView


def test_post_route_uses_post_view():
    url = reverse("blog:post")
    assert url == "/post/"
    assert resolve(url).func.view_class is PostView


def test_post_view_returns_hello_world(client):
    response = client.get(reverse("blog:post"))
    assert response.status_code == 200
    assert response.content.decode("utf-8") == "Hello World"
    assert response["Content-Type"] == "text/plain; charset=utf-8"


def test_post_view_rejects_unsupported_method(client):
    response = client.post(reverse("blog:post"))
    assert response.status_code == 405
