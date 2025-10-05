# Briefer — Especificação do Dashboard

## Páginas
1) **Visão Geral**
   - KPIs: total de alertas, média de score, top classes.
   - Série temporal por dia.

2) **Alertas**
   - Tabela com filtros: data, score (>=), classe.
   - Colunas: alert_id, source_id, timestamp, cls, score, snapshot_path.

3) **Evidências**
   - Galeria usando `snapshot_path` com tooltip (score/cls).

4) **Métricas**
   - Distribuição de `cls` e histograma de `score`.

## Dataset esperado
- `data/alerts.parquet` (preferencial) ou `data/alerts.csv`.
- Colunas conforme `briefer/schema.md`.
