# ODS 16 — Detecção e Dashboard Local (Briefer)
<img width="1359" height="613" alt="image" src="https://github.com/user-attachments/assets/8b96c4b8-d044-4bf5-b105-89e137a604ae" />

Projeto alinhado ao **ODS 16 — Paz, Justiça e Instituições Eficazes**.  
A solução é composta por:
- **Backend local (pipeline offline em Python)**: processa imagens/vídeos, executa a rede neural (ex.: YOLO), pós-processa e exporta resultados tabulares + *snapshots*.
- **Frontend local (Briefer)**: consome os arquivos gerados e oferece visão analítica (alertas, evidências e métricas).

> **Importante:** a inferência **não roda** dentro do Briefer. O Briefer é o **consumidor/visualizador**.  
> **Fluxo correto:** `pipeline (Python) → data/alerts.parquet|csv + snapshots/ → Briefer (dashboard local)`.

---

## Sumário
- [Arquitetura (visão rápida)](#arquitetura-visão-rápida)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Documentos por Sprint (Scrum)](#documentos-por-sprint-scrum)
- [Instalação](#instalação)
- [Execução do pipeline](#execução-do-pipeline)
- [Visualização no Briefer](#visualização-no-briefer)
- [Esquema de dados (mínimo)](#esquema-de-dados-mínimo)
- [Testes](#testes)
- [Gestão no GitHub Projects](#gestão-no-github-projects)
- [Roadmap do TP3 (Sprint em andamento)](#roadmap-do-tp3-sprint-em-andamento)
- [Contribuição e branches](#contribuição-e-branches)
- [Histórico de versões](#histórico-de-versões)
- [Integrante](#integrante)

---

## Arquitetura (visão rápida)

**Fluxo:** `pipeline (Python) → data/alerts.parquet|csv + snapshots/ → Briefer (dashboard local)`  
**Documentação detalhada (C4 Model):** `docs/arquitetura/TP2_ARQUITETURA.md`  
**Diagramas (PNG):** `figuras/`

- **Pipeline offline**: `pipeline/run.py` orquestra  
  `steps/load.py → steps/detect.py → steps/postprocess.py → steps/export.py`.
- **Briefer**: especificação de páginas/filtros/colunas em  
  `briefer/dashboard_spec.md` e `briefer/schema.md`.

---

## Estrutura de pastas

assets/ # logos/ícones (opcional)
briefer/ # especificação do dashboard (páginas, filtros, colunas)
data/ # entradas e saídas .parquet/.csv (geradas pelo pipeline)
docs/
arquitetura/ # TP2_ARQUITETURA.md (C4, decisões)
tp1/ # TP1_PLANEJAMENTO.md — artefatos do Sprint 1 (criar/mover aqui)
tp3/ # TP3_NOTAS.md — diário e decisões do Sprint 3 (criar)
figuras/ # diagramas C4 e de fluxo (PNG)
help/ # notas auxiliares (opcional)
pipeline/
run.py
steps/
load.py
detect.py
postprocess.py
export.py
snapshots/ # imagens recortadas geradas pelo pipeline
src/ # rascunhos/experimentos (opcional)
tests/ # testes (pytest)
CITATION.cff
README.md
config.yaml
requirements.txt

markdown
Copiar código

---

## Documentos por Sprint (Scrum)

- **TP1 — Definição do Problema e Planejamento Inicial**  
  - *O que contém:* ODS escolhido, problema, tipo de solução, RF/RNF, casos de uso e planejamento inicial.  
  - *Onde está:* `docs/tp1/TP1_PLANEJAMENTO.md` *(criar e mover seus artefatos do sprint 1 para cá).*  

- **TP2 — Projeto de Software (Arquitetura/C4)**  
  - *O que contém:* Arquitetura no C4 (Context e Container; Component opcional), decisões tecnológicas, justificativas.  
  - *Onde está:* `docs/arquitetura/TP2_ARQUITETURA.md` + diagramas em `figuras/`.  

- **TP3 — Sprint de Desenvolvimento (em andamento)**  
  - *O que conterá:* anotações de implementação, ajustes, decisões, impedimentos e links para PRs.  
  - *Onde registrar:* `docs/tp3/TP3_NOTAS.md`.

> Dica: cada sprint deve ter **um documento único** com os artefatos principais e referências (issues/PRs/commits).

---

## Instalação

Requisitos: **Python 3.10+**  
Para usar GPU, instale `torch/torchvision` conforme o site oficial do PyTorch **antes** do `ultralytics`.

```bash
git clone https://github.com/RhudsonDouglas/ods16-deteccao-armas-dashboard.git
cd ods16-deteccao-armas-dashboard

python3 -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\activate

pip install -r requirements.txt
Configuração (config.yaml, na raiz):

yaml
Copiar código
input_dir: "data"          # onde estão as imagens/vídeos ou dataset de entrada
output_dir: "data"         # onde o pipeline escreverá alerts.parquet/csv
snapshots_dir: "snapshots" # onde salvará as imagens recortadas

model_name: "yolov8n.pt"
confidence_threshold: 0.4
iou_threshold: 0.5

export_parquet: true
export_csv: true
Execução do pipeline
Coloque algumas imagens de teste (ou sua base) em data/.

Rode o pipeline:

bash
Copiar código
python -m pipeline.run --config config.yaml
Saídas esperadas:

data/alerts.parquet e/ou data/alerts.csv

snapshots/alert_000001.jpg (e outros)

Visualização no Briefer
Abra o Briefer local.

Importe data/alerts.parquet (ou data/alerts.csv).

Monte as páginas conforme briefer/dashboard_spec.md:

Visão Geral: KPIs (total de alertas, média de score), série temporal.

Alertas: tabela com filtros (data, score mínimo, classe).

Evidências: galeria com snapshot_path.

Métricas: distribuição de cls, histograma de score.

O arquivo briefer/schema.md documenta as colunas obrigatórias.

Esquema de dados (mínimo)
Campos esperados pelo dashboard no Briefer (colunas do alerts.parquet/csv):

csharp
Copiar código
alert_id (int)
source_id (string)
timestamp (datetime|null)
cls (int|string)
score (float)
bbox_xmin (float|int)
bbox_ymin (float|int)
bbox_xmax (float|int)
bbox_ymax (float|int)
snapshot_path (string|null)
Testes
Executar testes:

bash
Copiar código
pytest -q
Teste mínimo em tests/test_schema.py valida a presença das colunas obrigatórias.

Gestão no GitHub Projects
Mantenha as colunas: Project Backlog, TODO, In Progress, Done.

Mover para TODO no início do TP3:

Estruturar repositório para TP3
Done quando: pastas criadas/atualizadas; README.md, .gitignore, requirements.txt, config.yaml; docs/arquitetura/TP2_ARQUITETURA.md; diagramas em figuras/.

Implementar CLI do pipeline (pipeline/run.py com --config)
Done quando: orquestra steps, gera data/alerts.parquet|csv e snapshots/.

Integrar rede neural (YOLO) (steps/detect.py)
Done quando: retorna bboxes+scores; thresholds/IoU lidos de config.yaml.

Pós-processamento e exportação (steps/postprocess.py, steps/export.py)
Done quando: NMS/filtros aplicados; schema validado; snapshots salvos.

Dashboard no Briefer (briefer/dashboard_spec.md)
Done quando: páginas (Visão Geral, Alertas, Evidências, Métricas) definidas e protótipo funcionando com dataset gerado.

Qualidade (tests + schema) (tests/test_schema.py)
Done quando: pytest rodando e checando colunas mínimas.

Empacotamento e docs de uso (README.md)
Done quando: passo a passo pipeline→Briefer completo e revisado.

Itens fora do escopo do TP3 (ex.: anotação manual de FP/FN, tuning avançado, suporte a vídeo com extração de frames) permanecem em Project Backlog.

Roadmap do TP3 (Sprint em andamento)
 CLI do pipeline funcional (python -m pipeline.run --config config.yaml).

 YOLO integrado e configurável (modelo/thresholds/IoU).

 Exportação de alerts.parquet|csv + snapshots/.

 Dashboard no Briefer montado (4 páginas).

 Testes mínimos no pytest.

 README e docs atualizados.

Contribuição e branches
Branches curtos por tarefa (ex.: feat/pipeline-cli, feat/yolo-detect, docs/tp2-arquitetura).

Commits no padrão Conventional Commits (ex.: feat: CLI do pipeline com --config).

Tags:

v0.2.0 — TP2 publicado (arquitetura + esqueleto).

v0.3.0 — Entregável do TP3 (pipeline + dashboard local).

Histórico de versões
0.2.0 — TP2 publicado: arquitetura (C4), estrutura para pipeline offline e dashboard local no Briefer.

0.1.1 — Atualização de documentação (modelo anterior).

0.1.0 — Protótipo inicial de preparação de dados.

0.0.1 — Estrutura inicial do repositório.

Integrante
Rhudson Sampaio
