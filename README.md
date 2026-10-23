# Meu Blog — Django Admin

Atividade de Django Admin da EBAC (Exercício Módulo 10 na plataforma,
identificado como M52 neste repositório).

Esta entrega continua o projeto aprovado de Django Views:
[m51-meu-blog, Pull Request #1](https://github.com/mtgbcma-dotcom/m51-meu-blog/pull/1),
branch `views`, commit `e9ea518e93ac92b2cad188c7d0a03c7e69e3518b`.

## Funcionalidades preservadas

- Modelo `blog.Post`, seus campos e a migração inicial.
- `/post/`: `PostView.get()` retorna `Hello World`; métodos não implementados retornam 405.
- `/`: lista posts publicados, oculta rascunhos e publicações futuras e escapa HTML.
- Método `Post.publish()` e ação de publicação em lote no Admin.
- Os 12 testes originais, preservados sem alterações.

## Administração de posts

Em `/admin/`, um superusuário pode cadastrar, editar e excluir posts.
A listagem mostra título, autor, indicação de publicação, data de criação e data
de publicação. Há pesquisa por título e conteúdo, filtros por publicação, autor
e data de publicação e navegação pela data de criação. As datas de criação e
atualização são somente leitura.

Um post está publicado quando `published_at` está preenchido e não está no futuro,
seguindo a mesma regra da página inicial. O filtro "Não publicados" reúne rascunhos
e posts agendados. A ação "Publicar posts selecionados" publica os registros
selecionados e permite vê-los na página inicial.

## Executar no Windows / PowerShell

Use Python 3.10 ou superior. As versões de Django e das ferramentas de teste são
as mesmas da base aprovada, declaradas em `requirements.txt`.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Abra http://127.0.0.1:8000/admin/, entre com o superusuário e cadastre dois posts:
um sem data de publicação e outro com data de publicação no passado. Confira a
pesquisa e os filtros no Admin e a listagem em http://127.0.0.1:8000/.
A rota http://127.0.0.1:8000/post/ continua retornando `Hello World`.

O banco SQLite é local e não é versionado. Esta versão usa o app aprovado `blog`;
registros de um banco da antiga estrutura independente `publicacoes` não são
convertidos automaticamente. Para reproduzir a avaliação, utilize uma cópia limpa
do projeto e execute as migrações acima.

## Testes e verificações

```powershell
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe -m pip check
```

Suíte validada com Python 3.13: **26 testes aprovados**. São os 12 testes da base
aprovada e 14 casos adicionais do Admin: controle de acesso, listagem, cadastro,
edição, exclusão, pesquisa por título/conteúdo, filtros por publicação/autor,
navegação por data, publicação pela ação do painel e validação de título obrigatório.
Os testes usam um banco separado do banco local de desenvolvimento.

## Continuidade e entrega

A comparação dos arquivos preservados está em [docs/CONTINUIDADE.md](docs/CONTINUIDADE.md).
Esta correção substitui a estrutura independente anterior pela base aprovada e
adiciona a administração de posts sem alterar o modelo e as rotas anteriores.

Branch de entrega: `django-admin`. O [Pull Request #1](https://github.com/mtgbcma-dotcom/m52-django-admin/pull/1)
permanece aberto para avaliação da tutoria.
