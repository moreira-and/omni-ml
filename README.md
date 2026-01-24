# omni-ml

Base modular para projetos de Machine Learning com foco em **extração de dados externos** e organização em camadas (domínio, aplicação e infraestrutura). A proposta é oferecer uma fundação sustentável para evolução de pipelines analíticos, mantendo o domínio independente de detalhes técnicos.

---

## Visão geral da arquitetura

A estrutura segue princípios de DDD e Clean Architecture:

- **Domínio (`src/external_data/domain`)**: entidades, value objects, enums, eventos e modelos de domínio.
- **Aplicação (`src/external_data/application`)**: casos de uso e contratos (interfaces) que orquestram o fluxo.
- **Infraestrutura (`src/external_data/infrastructure`)**: integração com APIs externas, armazenamento e repositórios.
- **CLI (`src/external_data/cli`)**: ponto de entrada que monta dependências (composition root).

As dependências sempre apontam para dentro: infraestrutura depende de aplicação e domínio; aplicação depende apenas do domínio; domínio não depende de nada externo.

---

## Fluxo principal (extração)

1. **CLI** inicia a execução.
2. O **composition root** monta repositórios, resolvers e storages.
3. `ExecuteAllExtractions` coordena o ciclo:
   - lista definições
   - resolve parâmetros
   - executa extração em lote
   - persiste os resultados

---

## Estrutura do projeto

```
├── LICENSE
├── Makefile
├── README.md
├── config/
├── docker/
│   ├── docker-compose.yml
│   └── dockerfile.api
├── pyproject.toml
├── poetry.lock
├── setup.cfg
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── external_data/
│       ├── cli/
│       ├── domain/
│       ├── application/
│       └── infrastructure/
└── tests/
    ├── external_data/
    │   └── test_usecases.py
    ├── test_true.py
    └── test_training.py
```

---

## Execução local

### Pré-requisitos

- Python 3.10+
- Poetry

### Instalação

```bash
poetry config virtualenvs.in-project true --local
poetry install
```

### Executar a CLI de extração

```bash
python -m src.external_data.cli.main
```

---

## Docker

```bash
make up
```

Para parar ou limpar:

```bash
make down
make clean
```

---

## Testes

```bash
pytest tests/external_data/test_usecases.py
```

> Observação: `tests/test_training.py` referencia módulos ainda não presentes em `src/`. Ajuste ou remova se precisar de uma suíte consistente.

---

## Como evoluir

- Novos extractors devem implementar `ExtractExecutor` na camada de infraestrutura.
- Novos params devem ser modelados no domínio e resolvidos via `ExtractParamsResolver`.
- Novos storages devem implementar `ExtractResultStore`.

Mais detalhes estão em `CONTRIBUTING.md`.
