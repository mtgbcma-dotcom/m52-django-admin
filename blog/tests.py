import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from .models import Post


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create_user(username="bruno", password="test-only")


@pytest.fixture
def post(author):
    return Post.objects.create(title="Meu primeiro post", content="Aprendendo Django.", author=author)


@pytest.mark.django_db
def test_post_is_saved_with_its_attributes(post, author):
    saved = Post.objects.get(pk=post.pk)
    assert saved.title == "Meu primeiro post"
    assert saved.content == "Aprendendo Django."
    assert saved.author == author
    assert saved.created_at is not None
    assert saved.updated_at is not None
    assert saved.published_at is None


@pytest.mark.django_db
def test_post_string_is_its_title(post):
    assert str(post) == "Meu primeiro post"


@pytest.mark.django_db
def test_publish_persists_publication_date(post):
    before = timezone.now()
    post.publish()
    post.refresh_from_db()
    assert before <= post.published_at <= timezone.now()
    assert post.updated_at >= post.created_at


@pytest.mark.django_db
def test_posts_are_ordered_newest_first(post, author):
    newer = Post.objects.create(title="Segundo post", content="Outro texto", author=author)
    assert list(Post.objects.all()) == [newer, post]


@pytest.mark.django_db
def test_title_longer_than_200_characters_is_invalid(author):
    invalid = Post(title="x" * 201, content="Texto", author=author)
    with pytest.raises(ValidationError) as error:
        invalid.full_clean()
    assert "title" in error.value.message_dict


@pytest.mark.django_db
def test_blank_content_is_invalid(author):
    invalid = Post(title="Título", content="", author=author)
    with pytest.raises(ValidationError) as error:
        invalid.full_clean()
    assert "content" in error.value.message_dict


@pytest.mark.django_db
def test_deleting_author_deletes_related_posts(post, author):
    post_id = post.pk
    author.delete()
    assert not Post.objects.filter(pk=post_id).exists()


@pytest.mark.django_db
def test_home_only_shows_published_posts(client, post, author):
    published = Post.objects.create(title="Texto publicado", content="Conteúdo público", author=author)
    published.publish()
    Post.objects.create(title="Texto futuro", content="Agendado", author=author,
                        published_at=timezone.now() + timezone.timedelta(days=1))
    response = client.get(reverse("blog:post_list"))
    assert response.status_code == 200
    assert list(response.context["posts"]) == [published]
    assert "Texto publicado" in response.content.decode()
    assert post.title not in response.content.decode()
    assert "Texto futuro" not in response.content.decode()


@pytest.mark.django_db
def test_home_escapes_post_content(client, author):
    post = Post.objects.create(title="HTML", content="<script>alert(1)</script>", author=author)
    post.publish()
    html = client.get(reverse("blog:post_list")).content.decode()
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html
