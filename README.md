# Pega_voo - Sistema de Reserva de Passagens Aéreas

## Como Rodar o Projeto

O projeto está configurado para rodar completamente através do Docker Compose. Siga os passos abaixo:

### 1. Configurar Variáveis de Ambiente

Antes de iniciar, crie um arquivo `.env` na raiz do projeto baseado no `.env.example`,
verifique tambem o docker compose, pois algumas linhas estao comentadas, no projeto utilizamos postgres 17 para os testes,
mas trocamos para o supabase proximo da entrega, bem como o frontenv foi hospedado o front end na vercel, sendo necessario somente o endereco do backend para utilizar dos outros servicos.

o backend utliza do celery para algumas tarefas, como criacao e envio de emails, bem como codigos de otp, 
para recuperacao de contas, para que eles funcionem corretamente e preciso utilizar o celery instanciado com o redis como broker,
para fins de avaliacao, deixei o .example com as variaveis que utilizamos, retirando somente algumas particulares, como senha de gmail app, senha do redis, chaves do stripe e os dados do supabase.

preencher a variavel senha no redis, caso esteja vazia durante a criacao, o celery ira falhar pois depende do redis ativo para operar.
backend e front possuem arquivos proprios para caso necessite subir apenas um deles.

caso utilize um novo banco de dados via docker, precisa subir a migracao via alembic, na pasta do backend ja tem tudo configurado, basta iniciar o venv e executar 

```python
alembic upgrade head
```

### 2. Iniciar os Serviços


```bash
docker-compose up -d
```

Isso iniciará todos os serviços definidos em `Docker-compose.yml`:

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| **db** | 5432 | PostgreSQL |
| **broker** | 6379 | Redis |
| **api** | 8000 | FastAPI  |
| **worker** | * | Celery |
| **web** | 3000 | Nuxt |

### 3. Acessar a Aplicação

- **Frontend**: http://localhost:3000
- **API**: http://localhost:7777
- **Docs API**: http://localhost:7777/docs ou /redoc


## Estrutura do Projeto

- **src/tinto_api/**: Backend em python 3.12.10 com FastAPI, postgresql, Celery, Psycopg2 e Redis
- **src/web/**: Frontend em nodejs 24.11.1 com Nuxt 3 e TailwindCSS
- **docs/**: Documentação da aplicação (DER, ER, atas de de reuniao, etc..)
