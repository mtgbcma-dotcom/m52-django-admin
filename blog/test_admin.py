import pytest
from django.urls import reverse
from django.utils import timezone

from .models import Post


pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_user(django_user_model):
    return django_user_model.objects.create_superuser(
        username="admin", email="admin@example.com", password="test-only"
    )


@pytest.fixture
def admin_client(client, admin_user):
    client.force_login(admin_user)
    return client


@pytest.fixture
def posts(admin_user, django_user_model):
    other = django_user_model.objects.create_user(username="other", password="test-only")
    published = Post.objects.create(
        title="Publicado", content="Conteúdo disponível", author=admin_user,
        published_at=timezone.now() - timezone.timedelta(days=1),
    )
    draft = Post.objects.create(title="Rascunho", content="Texto reservado", author=other)
    future = Post.objects.create(
        title="Agendado", content="Conteúdo futuro", author=admin_user,
        published_at=timezone.now() + timezone.timedelta(days=1),
    )
    return published, draft, future


def test_admin_requires_login(client):
    url = reverse("admin:blog_post_changelist")
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse("admin:login") + "?next=" + url


def test_regular_user_cannot_access_admin(client, django_user_model):
    user = django_user_model.objects.create_user(username="reader", password="test-only")
    client.force_login(user)
    response = client.get(reverse("admin:blog_post_changelist"))
    assert response.status_code == 302
    assert response.url.startswith(reverse("admin:login"))


def test_admin_lists_drafts_published_and_scheduled_posts(admin_client, posts):
    response = admin_client.get(reverse("admin:blog_post_changelist"))
    assert response.status_code == 200
    assert set(response.context["cl"].queryset) == set(posts)
    model_admin = response.context["cl"].model_admin
    assert [model_admin.is_published(post) for post in posts] == [True, False, False]


def test_admin_creates_post_without_changing_previous_routes(admin_client, admin_user):
    response = admin_client.post(reverse("admin:blog_post_add"), {
        "title": "Novo post pelo Admin", "content": "Texto cadastrado pelo painel",
        "author": admin_user.pk, "published_at_0": "", "published_at_1": "",
        "_save": "Salvar",
    })
    assert response.status_code == 302
    post = Post.objects.get(title="Novo post pelo Admin")
    assert post.author == admin_user
    assert post.content == "Texto cadastrado pelo painel"
    assert post.published_at is None
    assert admin_client.get(reverse("blog:post")).content == b"Hello World"
    home = admin_client.get(reverse("blog:post_list"))
    assert post not in list(home.context["posts"])


def test_admin_edits_post_and_preserves_creation_date(admin_client, posts):
    published, _, _ = posts
    created_at = published.created_at
    response = admin_client.post(reverse("admin:blog_post_change", args=[published.pk]), {
        "title": "Título editado", "content": "Conteúdo editado",
        "author": published.author_id, "published_at_0": "", "published_at_1": "",
        "created_at": "2000-01-01", "updated_at": "2000-01-01", "_save": "Salvar",
    })
    assert response.status_code == 302
    published.refresh_from_db()
    assert published.title == "Título editado"
    assert published.content == "Conteúdo editado"
    assert published.created_at == created_at
    assert published.updated_at > created_at
    assert published.published_at is None


def test_admin_deletes_post(admin_client, posts):
    _, draft, _ = posts
    response = admin_client.post(
        reverse("admin:blog_post_delete", args=[draft.pk]), {"post": "yes"}
    )
    assert response.status_code == 302
    assert not Post.objects.filter(pk=draft.pk).exists()


@pytest.mark.parametrize("query", ["Publicado", "disponível"])
def test_admin_searches_title_and_content(admin_client, posts, query):
    response = admin_client.get(reverse("admin:blog_post_changelist"), {"q": query})
    assert response.status_code == 200
    assert list(response.context["cl"].queryset) == [posts[0]]


@pytest.mark.parametrize("status,indices", [("published", [0]), ("unpublished", [1, 2])])
def test_admin_filters_publication_status(admin_client, posts, status, indices):
    response = admin_client.get(
        reverse("admin:blog_post_changelist"), {"publication_status": status}
    )
    assert response.status_code == 200
    assert set(response.context["cl"].queryset) == {posts[index] for index in indices}


def test_admin_filters_author(admin_client, posts):
    _, draft, _ = posts
    response = admin_client.get(
        reverse("admin:blog_post_changelist"), {"author__id__exact": draft.author_id}
    )
    assert response.status_code == 200
    assert list(response.context["cl"].queryset) == [draft]


def test_admin_navigates_creation_date(admin_client, posts):
    day = timezone.localtime(posts[0].created_at).date()
    response = admin_client.get(reverse("admin:blog_post_changelist"), {
        "created_at__year": day.year, "created_at__month": day.month,
        "created_at__day": day.day,
    })
    assert response.status_code == 200
    assert set(response.context["cl"].queryset) == set(posts)


def test_publish_action_keeps_original_model_and_makes_post_visible(admin_client, posts):
    _, draft, _ = posts
    response = admin_client.post(reverse("admin:blog_post_changelist"), {
        "action": "publish_posts", "_selected_action": [draft.pk], "index": "0",
    })
    assert response.status_code == 302
    draft.refresh_from_db()
    assert draft.published_at is not None
    home = admin_client.get(reverse("blog:post_list"))
    assert draft in list(home.context["posts"])
    assert draft.title in home.content.decode("utf-8")


def test_admin_rejects_post_without_title(admin_client, admin_user):
    response = admin_client.post(reverse("admin:blog_post_add"), {
        "title": "", "content": "Texto", "author": admin_user.pk,
        "published_at_0": "", "published_at_1": "", "_save": "Salvar",
    })
    assert response.status_code == 200
    assert "title" in response.context["adminform"].form.errors
    assert not Post.objects.exists()
