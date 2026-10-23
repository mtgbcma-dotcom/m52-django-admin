# Continuidade do projeto aprovado

Base: https://github.com/mtgbcma-dotcom/m51-meu-blog/pull/1

Branch: `views`.

Commit de referência: `e9ea518e93ac92b2cad188c7d0a03c7e69e3518b`.

A correção foi aplicada à branch `django-admin` do Pull Request #1 do repositório
`m52-django-admin`, preservando o histórico existente, sem reescrever commits.

## Arquivos preservados sem alterações

- `blog/models.py`
- `blog/migrations/0001_initial.py` e `blog/migrations/__init__.py`
- `blog/views.py`
- `blog/urls.py`
- `blog/tests.py`
- `blog/test_views.py`
- `blog/templates/blog/post_list.html`
- `blog/apps.py` e `blog/__init__.py`
- `config/settings.py`, `config/urls.py`, `config/asgi.py`, `config/wsgi.py` e `config/__init__.py`
- `manage.py`, `requirements.txt`, `pytest.ini` e `.gitignore`

Os arquivos acima foram comparados byte a byte com o commit de referência.
Os 12 testes da base foram executados antes da integração e preservados na suíte final.

## Alterações desta atividade

- `blog/admin.py`: mantém o registro original e a ação `publish_posts` e acrescenta
  indicação de publicação, filtro de publicados/não publicados, navegação por data,
  datas de criação/atualização somente leitura e carregamento conjunto do autor.
- `blog/test_admin.py`: 14 casos de integração que exercitam o painel administrativo
  e sua relação com as páginas anteriores.
- `README.md`: instruções de execução, testes, uso do Admin e identificação da base.
- Remoção do app independente `publicacoes`, substituído pelo app aprovado `blog`.
  Nenhum banco SQLite é incluído no repositório; a migração original de `blog` é mantida.

Não foi criado outro modelo `Post` e não foi necessário alterar a migração da base.

## Validação

- Base aprovada: 12 testes aprovados.
- Entrega corrigida: 26 testes aprovados (12 originais + 14 de Admin).
- `manage.py check`: nenhum problema.
- `manage.py makemigrations --check --dry-run`: nenhuma mudança pendente.
- `pip check`: dependências compatíveis.

As verificações foram realizadas com Python 3.13, Django 5.2.18, pytest 9.1.1 e
pytest-django 4.14.0. A evidência anterior do painel `publicacoes` foi substituída
na descrição do Pull Request pelo relato da implementação e das verificações
da versão que usa `blog.Post`.
