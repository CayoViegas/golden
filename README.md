# Golden API

Uma API RESTful desenvolvida com **FastAPI** e **SQLAlchemy 2.0**, construída com foco em **Qualidade de Software**, **Testes Automatizados** e **Integração Contínua (CI/CD)**.

O objetivo deste projeto é demonstrar a implementação de uma arquitetura escalável (separação por camadas) aliada a um *Quality Gate* extremamente estrito, garantindo um código sustentável e à prova de regressões.

## Tecnologias e Stack

- **Framework:** FastAPI (Python 3.10)
- **Banco de Dados:** PostgreSQL (containerizado)
- **ORM & Migrations:** SQLAlchemy 2.0 + Alembic
- **Validação:** Pydantic v2
- **Ambiente:** Docker & Docker Compose

---

## Foco em Qualidade (QA & CI/CD)

Este projeto foi arquitetado com a mentalidade de *Shift-Left Testing*, garantindo qualidade desde a escrita do código até o deploy.

* **100% de Test Coverage:** Cobertura completa de testes unitários e de integração utilizando `pytest`. Cada rota, serviço e modelo de banco de dados é validado.
* **Dados Dinâmicos nos Testes:** Utilização da biblioteca `Faker` para geração de payloads dinâmicos, evitando o vício de *hardcoded strings* e descobrindo *edge cases* reais.
* **Isolamento de Estado:** Configuração avançada do `conftest.py` com injeção de dependências (`dependency_overrides`), rodando testes em um banco SQLite em memória que é limpo a cada função, eliminando o *flakiness*.
* **Linting e Formatação Extremos:** Adoção do `Ruff` (linter em Rust) para checagem estática, detecção de bugs (Flake8-bugbear) e formatação de código, mantendo o padrão PEP-8.
* **Pre-commit Hooks:** Configuração de hooks locais que impedem *commits* de código não formatado ou com arquivos desnecessariamente pesados, economizando tempo de pipeline.
* **Continuous Integration (GitHub Actions):** Pipeline automatizada que atua como *Quality Gate*. Qualquer PR ou push precisa obrigatoriamente passar pelo `Ruff` (estilo) e pelo `Pytest` (comportamento).

---

## Arquitetura

O projeto segue um padrão de camadas para facilitar o isolamento e o mock nos testes:

```text
app/
 ├── core/       # Configurações globais e segurança (Pydantic Settings)
 ├── db/         # Setup de conexão e injeção do SQLAlchemy
 ├── models/     # Entidades do banco de dados (ORM)
 ├── schemas/    # Contratos de dados de entrada/saída (Pydantic)
 ├── services/   # Regras de negócio isoladas (Totalmente testáveis sem HTTP)
 ├── routes/     # Endpoints do FastAPI (Controllers)
 └── tests/      # Suíte de testes (Pytest)
 ```

---

 ## Como Executar Localmente

 **Pré-requisitos**
 - Docker e Docker Compose instalados.

 **Passos**
 1. Clone o repositório e crie o arquivo de variáveis de ambiente:

 ```bash
 cp .env.example .env
 ```

 2. Suba a infraestrutura (Banco de Dados e Backend):

 ```bash
 docker compose up -d --build
 ```

 3. Execute as migrações para criar as tabelas no banco de dados:

 ```bash
 docker compose run --rm backend alembic upgrade head
 ```

 4. Acesse a documentação interativa (Swagger UI):

 - **URL:** http://localhost:8000/docs

---

 ## Como Rodar os Testes

 Para executar a suíte de testes e gerar o relatório de cobertura no terminal:

 ```bash
 docker compose run --rm backend pytest --cov=app --cov-report=term-missing
 ```

---

 ## Próximos Passos (Roadmap)

 - Integração do módulo de Autenticação/Autorização (JWT).
 - Implementação de Logs Estruturados (Observabilidade).
 - Construção do Frontend (React/Next.js) consumindo a API.
