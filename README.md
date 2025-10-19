# ODS 16 — Detecção e Dashboard Local (Briefer)

<img width="1359" height="613" alt="image" src="https://github.com/user-attachments/assets/8b96c4b8-d044-4bf5-b105-89e137a604ae" />

Projeto alinhado ao **ODS 16 — Paz, Justiça e Instituições Eficazes**.

A solução é composta por:
- **Backend local (pipeline offline em Python)** — processa mídia de entrada, executa a rede neural (ex.: YOLO), pós-processa e exporta `alerts.parquet|csv` + *snapshots*;
- **Frontend local (Briefer)** — consome os arquivos exportados e exibe visão analítica (KPIs, alertas, evidências e métricas).

> **Importante**: inferência **não roda** dentro do Briefer. Ele é o **visualizador**.
> **Fluxo correto**: `pipeline (Python) → data/alerts.parquet|csv + snapshots/ → Briefer (dashboard local)`.

---

## Sumário
- [Arquitetura (visão rápida)](#arquitetura-visão-rápida)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Instalação rápida](#instalação-rápida)
- [Execução (duas opções)](#execução-duas-opções)
- [Visualização no Briefer](#visualização-no-briefer)
- [Esquema de dados (mínimo)](#esquema-de-dados-mínimo)
- [Testes (mínimo)](#testes-mínimo)
- [Gestão no GitHub Projects](#gestão-no-github-projects)
- [Roadmap do TP3](#roadmap-do-tp3)
- [Histórico de versões](#histórico-de-versões)
- [Integrante](#integrante)

---

## Arquitetura (visão rápida)

**Fluxo:** `pipeline (Python) → data/alerts.parquet|csv + snapshots/ → Briefer (dashboard local)`

- **Pipeline**: `pipeline/run.py` orquestra `steps/load.py → steps/detect.py → steps/postprocess.py → steps/export.py`.
- **Briefer**: especificação de páginas/filtros/colunas em `briefer/dashboard_spec.md` e `briefer/schema.md`.

---

## Estrutura de pastas

assets/ # logos/ícones (opcional)
briefer/
dashboard_spec.md # páginas, filtros e campos (documentação)
schema.md # colunas mínimas esperadas pelo dashboard
make_briefer_everything.py # utilitário para gerar pacote p/ Briefer (demo/real)
data/
alerts.csv # saída do pipeline (exemplo/placeholder)
alerts.parquet # saída do pipeline (exemplo/placeholder)
docs/
arquitetura/
TP2_ARQUITETURA.md # C4 + decisões de tecnologia
tp1/TP1_PLANEJAMENTO.md # artefatos do sprint 1
tp3/TP3_NOTAS.md # diário do sprint 3 (decisões/impedimentos)
figuras/ # diagramas (PNG)
pipeline/
run.py
steps/
load.py
detect.py
postprocess.py
export.py
snapshots/ # snapshots recortados (gerados)
tests/
test_schema.py # teste mínimo do schema
requirements.txt
config.yaml
README.md

yaml
Copiar código

> Os arquivos sob `pipeline/` podem iniciar como *stubs* (esqueletos) e evoluem no TP4.

---

## Instalação rápida

Requisitos: **Python 3.10+**

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\activate

pip install -r requirements.txt
requirements.txt (mínimo):

nginx
Copiar código
numpy
pandas
pyarrow
pillow
requests
# Para detecção (TP4 em diante):
# ultralytics
# torch
# torchvision
