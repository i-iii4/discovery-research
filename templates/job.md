---
id: JOB-XXX
title: ""
audience: b2c            # b2c | b2b
pipelines: []            # кто трогал работу: market, jtbd (список — обогащается)
profile: saas            # saas | mobile-us
segment: ""
trigger: ""
desire: ""
job_type: ""             # частотная | разовая | фоновая
level: ""                # Core | под-работа
stage: ""                # обнаружена | оценена
verdict: ""              # ALIVE | WEAK | KILL — сводный по всем пайплайнам
severity:                # сводная острота 1-10
breadth:                 # сводный охват
frequency: ""
current_spend: ""
runs: []
parent_job: ""
related_jobs: []
hypotheses: []
tags:
  - job
---

## Формулировка (JTBD)
> Когда [контекст], я хочу [цель], чтобы [результат].

## Тип и уровень
**Тип:** …  **Уровень:** …  **Обоснование:** …

## Связи
Иерархия, КПР, связанные работы.

## Доказательства — jtbd
<!-- Заполняет 02-jtbd-b2c: Wave A/B, охват, острота, switching, RAT. Опустить, если пайплайн работу не трогал. -->

## Доказательства — market
<!-- Заполняет 01-market-b2c: demand-signal tier (T1-T3), веб-ссылки, конкуренты в сторе, рейтинги. Опустить, если не трогал. -->

## Как решают сейчас (workarounds)
| Инструмент | Статус | Причина отказа |
|---|---|---|
