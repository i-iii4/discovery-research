# Architecture: b2c-discovery-persona (v15-jtbd-only)

Related documents: [PLAN.md](PLAN.md) | [DEVLOG.md](DEVLOG.md) | [CLAUDE.md](CLAUDE.md) | [methodology.md](methodology.md) | [persona-protocol.md](persona-protocol.md) | [ajtbd-prompts.md](ajtbd-prompts.md)

## Context

Цель проекта не изменилась: найти жизнеспособные B2C jobs для solo-разработчика с горизонтом 2 недели до MVP и потенциалом до $5K/мес.

Изменение v15: убраны стартовые Scout-агенты и веб-поисковая генерация сигналов. Пайплайн стал полностью JTBD-центричным: сначала извлечение jobs через глубинные интервью, затем независимая валидация этих jobs второй волной интервью.

## Pipeline (v15-jtbd-only)

```
                 ┌──────────┐
                 │   LEAD   │ orchestrator (человек + Claude Code)
                 └────┬─────┘
                      │
        ┌─────────────▼─────────────┐
        │ R0 Domain Seed            │
        │ 1 область + 2-3 сегмента  │
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │ R1 Persona Panel A        │
        │ 8-10 персон (discovery)   │
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │ R2 Deep Interviews A      │
        │ Jobs + workarounds +      │
        │ switching signals         │
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │ R2.5 Job Synthesis        │
        │ Кластеры + shortlist 8-12 │
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │ R3 Persona Panel B        │
        │ 8-10 новых персон         │
        │ (без переиспользования A) │
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │ R4 Deep Interviews B      │
        │ Валид. jobs (двухагентно) │
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │ R4.5 Scoring + RAT        │
        │ Breadth/Severity/...      │
        └─────────────┬─────────────┘
                      │
                 ┌────▼─────┐
                 │    R5    │
                 │ Synthesis│
                 └────┬─────┘
                      │
         ┌────────────┴────────────┐
         │ OUTPUT 1: Validated Jobs│
         │ OUTPUT 2: Discovered Jobs│
         └────────────┬────────────┘
                      │
        Cycle N+1: Discovered Jobs -> R0 Domain Seed
```

## Stages

| # | Stage | Agent format | Model | Input | Output |
|---|-------|--------------|-------|-------|--------|
| R0 | Domain Seed | Lead + 1 helper | Sonnet | Founder profile + anti-domains | 1 domain, 2-3 subsegments, run scope |
| R1 | Persona Panel A | 1x | Sonnet | Domain seed | 8-10 discovery personas |
| R2 | Deep Interviews A | 2 parallel interview teams | Sonnet | Personas A | Raw jobs, workaround chains, switching stories |
| R2.5 | Job Synthesis | Lead + 1 helper | Sonnet | Interview transcripts A | 8-12 clustered jobs |
| R3 | Persona Panel B | 1x | Sonnet | Job shortlist | 8-10 validation personas (новая выборка) |
| R4 | Deep Interviews B | 2 parallel two-agent teams | Sonnet | Jobs + Personas B | Per-job validation evidence |
| R4.5 | Scoring + RAT | 1x | Sonnet | R4 evidence | Score 0-100 + Top-5 risks |
| R5 | Synthesis | Lead | — | R4.5 | Final dossier + cycle backlog |

## Design principles

1. JTBD-only: pipeline не зависит от web-search как входного фильтра.
2. Two-pass interviews: discovery и validation разделены по панелям.
3. Anti-bias by design: финальная валидация только через двухагентный формат.
4. Reproducibility: каждый этап оставляет отдельный артефакт в `runs/`.
5. Budget caps: у каждого этапа есть лимит токенов и early-stop.
6. Context discipline: полные интервью сохраняются в `runs/`, в чат возвращается только summary.

## Scoring (v15)

Используется единый panel score (0-100):

- Breadth (3x): сколько персон подтвердили job по фактам прошлого поведения
- Severity (2x): сила боли по конкретным эпизодам
- Frequency (2x): регулярность возникновения
- Current Spend (1x): фактические траты на workaround
- Switching History (1x): опыт смены инструментов в смежных задачах

Порог:
- `ALIVE`: >= 60
- `WEAK`: 40-59
- `KILL`: < 40

RAT (P x I) остаётся обязательным слоем:
- `RED FLAG`: любой риск > 20
- При `RED FLAG` итог не может быть выше `ALIVE (MODERATE)` без mitigation-плана

## Required controls

- R4 cannot be skipped. Если двухагентная валидация не выполнена, итог = `UNVALIDATED`.
- Persona leakage ban: персоны из Panel A не допускаются в Panel B.
- Domain randomization log: выбор домена фиксируется явно (`why this domain now`).
- Structured overrides: любой ручной override только с причиной в формате `override_reason`.

## Expected performance envelope

- Cycle runtime: 45-110 min (в зависимости от размера shortlist и числа интервью)
- Typical tokens: ~400K-800K per run
- Main quality KPI: доля `R2 -> R4` jobs, подтверждённых независимой панелью
- Method KPI: стабильность verdict distribution на 3 последовательных прогонах

## Change log marker

- v14-persona -> v15-jtbd-only: удалены Scout/Scout-C/Signal Gate и web-search-first логика.
- Core loop теперь: `Domain Seed -> Discovery Interviews -> Validation Interviews -> Synthesis`.
