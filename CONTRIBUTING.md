# Contributing

Este projeto prioriza uma base sólida de longo prazo, com separação clara entre domínio, aplicação e infraestrutura. As contribuições devem manter essa separação e preservar a linguagem ubíqua.

---

## Princípios arquiteturais

1. **Dependências sempre apontam para dentro**
   - `infrastructure -> application -> domain`
   - O domínio não importa nada de infraestrutura ou de frameworks.

2. **Domínio é o núcleo do negócio**
   - Entidades, value objects, enums e eventos vivem no domínio.
   - O domínio não conhece detalhes de persistência, rede ou bibliotecas externas.

3. **Aplicação orquestra, mas não executa detalhes técnicos**
   - Casos de uso coordenam o fluxo entre portas (interfaces) e o domínio.
   - Lógica técnica deve permanecer em adaptadores de infraestrutura.

4. **Infraestrutura é intercambiável**
   - Extractors, storages e repositórios são adapters e devem depender de interfaces da aplicação.

---

## Onde cada tipo de lógica deve viver

### Domain (`src/external_data/domain`)

- **Entidades**: regras e comportamento de conceitos do domínio (ex.: `ExtractDefinition`).
- **Value Objects**: validações e invariantes de tipos (ex.: `ExternalCode`, `InternalAlias`).
- **Eventos de domínio**: sinalizam ações relevantes do domínio (ex.: `ExtractRequested`).
- **Params e modelos**: estruturas que representam o estado do domínio.

> Evite colocar lógica técnica aqui (I/O, pandas, APIs externas).

### Application (`src/external_data/application`)

- **Casos de uso**: classes com intenção explícita (ex.: `ExecuteAllExtractions`).
- **Interfaces**: portas para repositórios, executores, storages.
- **Resolvers e clocks**: políticas de decisão e controle de tempo.

> Aplicação coordena, mas não sabe como os dados são extraídos ou persistidos.

### Infrastructure (`src/external_data/infrastructure`)

- **Extractors**: integrações concretas com fontes externas (YFinance, BCB etc.).
- **Storages**: persistência concreta (CSV, banco etc.).
- **Repositories**: leitura de definições e dados externos.

> Tudo que toca rede, disco ou bibliotecas externas pertence aqui.

---

## Como adicionar novos extractors

1. Crie uma classe em `src/external_data/infrastructure/extractors/`.
2. Implemente a interface `ExtractExecutor`.
3. Indique `source` e `data_kind` corretamente.
4. Registre o executor no `composition_root` (função `build_extract_executors`).

---

## Como adicionar novos params

1. Modele o novo param em `src/external_data/domain/params`.
2. Atualize o `ExtractParamsResolver` para resolver com base no `DataKind`.
3. Ajuste o extractor para aceitar o novo tipo de param.

---

## Como adicionar novos storages

1. Crie uma classe em `src/external_data/infrastructure/storage`.
2. Implemente a interface `ExtractResultStore`.
3. Atualize o `composition_root` para usar o storage desejado.

---

## Testes

- Casos de uso devem ter testes unitários em `tests/external_data/`.
- Preferir mocks para infraestrutura (evite I/O real nos testes de aplicação).
- Garanta que o domínio continue livre de dependências externas.

---

## O que evitar

- Importar infra dentro de domínio ou aplicação.
- Colocar decisões de negócio dentro de adaptadores técnicos.
- Acoplar use cases a bibliotecas específicas.

---

## Revisão antes do PR

- [ ] O domínio continua independente?
- [ ] A aplicação só orquestra?
- [ ] A infraestrutura é intercambiável?
- [ ] Testes cobrem a nova lógica?
