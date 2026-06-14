# Implementation Plan

Related documents: [ARCHITECTURE.md](ARCHITECTURE.md) | [DEVLOG.md](DEVLOG.md) | [CLAUDE.md](CLAUDE.md) | [methodology.md](methodology.md)

## Goal

Прогнать пайплайн v10 10-30 раз, накопить ~100 выживших гипотез. Затем — отдельный фреймворк для второго этапа валидации (другой проект).

Definition of done: v12 стабильно работает, результаты каждого прогона в results.md.

## Phases

### Phase 1 — Доработки методологии v6 → v7 [DONE]

Goal: внести изменения в methodology.md на основе аудита.

| # | Task | Status |
|---|------|--------|
| 1.1 | T1-alt: добавить workaround chains как эквивалент T1 для novel categories | [x] |
| 1.2 | Убрать "ADHD audience" из whitelist (оставить органическое появление через Scout) | [x] |
| 1.3 | Заменить бинарный FREE auto-kill на оценку job overlap | [x] |
| 1.4 | Red Team agent: devil's advocate для structural risks | [x] |
| 1.5 | Обновить заголовок v5 → v7, Quick Start, pipeline flow | [x] |
| 1.6 | Lessons learned 27-31 | [x] |
| 1.7 | Добавить Discord в Scout sources | [x] |
| 1.8 | Понизить приоритет PH-сигналов (только EMERGING, не DEMAND) | [x] |
| 1.9 | Исправить нумерацию правил генератора (было: 1-6, 8, 9, 10, 7) | [x] |
| 1.10 | Убрать build plan / next steps / Round 5 из Synthesis и методологии | [x] |
| 1.11 | Ревизия blacklist: проверить актуальность позиций из v1 | [x] (все актуальны) |

### Phase 1.5 — v8: Rule Compliance Check [DONE]

Goal: автоматизировать проверку правил после Generator, добавить ADHD blacklist.

| # | Task | Status |
|---|------|--------|
| 1.5.1 | ADHD/ND в полный blacklist (#15) | [x] |
| 1.5.2 | Rule Compliance Check (R1.5): Haiku-агент для blacklist/factcheck/diversity | [x] |
| 1.5.3 | App Store scan в Quick Validator (4-й запрос) | [x] |
| 1.5.4 | Запуск v8-run1 | [x] — 2 MODERATE (StudioQueue, ReadStash) |
| 1.5.5 | Досье финалистов в finalists/ (14 файлов) | [x] |

### Phase 1.6 — v9: оптимизация качества и токенов [DONE]

Goal: снизить расход токенов на 30-40% без потери качества. На основе мета-анализа v8-run1.

| # | Task | Status |
|---|------|--------|
| 1.6.1 | Scout-B: убрать PRICING_GAP полностью, снизить до 10-15 сигналов | [x] |
| 1.6.2 | Generator: 25 → 20 гипотез | [x] |
| 1.6.3 | Rule Check: Pattern Cap enforcement (FLAG → KILL) | [x] |
| 1.6.4 | Rule Check: Free Alternative Pre-screen (1 search per hyp) | [x] |
| 1.6.5 | Critic: 3 → 2-3 агента (2 при <8 гипотез) | [x] |
| 1.6.6 | Deep Validator: RED FLAG skip rule | [x] |
| 1.6.7 | Budget table: обновить с v9 estimates | [x] |
| 1.6.8 | DEVLOG entry | [x] |

### Phase 2 — Запуски v9 [DONE]

Goal: прогонять пайплайн v9, накапливая гипотезы. Каждый прогон = отдельная запись в DEVLOG и results.md.

| # | Task | Status |
|---|------|--------|
| 2.1 | Запуск v9 run 1 | [x] — 0 finalists (H20 QSExport WEAK) |
| 2.2 | Сохранить артефакты в runs/v9-run1/ | [x] — 7 файлов (round-0 through round-4) |
| 2.3 | Обновить results.md + DEVLOG | [x] |
| 2.4 | Анализ: v9 vs v8 (token savings, kill rate, verdict distribution) | [x] — см. ниже |
| 2.5 | Калибровка: подтвердить 30-40% экономию токенов | [x] — НЕТ, расход вырос: 393K vs 300K (v8) |
| 2.6 | Запуск v9 run 2 | [x] — 0 finalists (H16 SheetSync WEAK), ~330K tokens |
| 2.7 | Запуск v9 run 3 | [x] — **1 STRONG (H20 WorkBench 8/12)**, ~480K tokens |
| 2.8 | Запуск v9 run 7 | [x] — 0 finalists, ~263K tokens. 100% kill rate |

> v9 итого: 7 прогонов, 1 STRONG (WorkBench), 5 пустых. Efficiency: ~2.3M/финалист — worst.
> Корневая причина: input quality (устаревшие сигналы, Generator в зрелых рынках).
> Решение: обновление до v10 (Phase 2.5).

### Phase 2.5 — v10: input quality [DONE]

Goal: исправить три корневые причины пустых прогонов v9.

| # | Task | Status |
|---|------|--------|
| 2.5.1 | Scout freshness check: 1 доп. поиск на сигнал старше 6 мес | [x] |
| 2.5.2 | Competition Pre-screen в Rule Check: 1 поиск на гипотезу | [x] |
| 2.5.3 | Расширить Saturated Market Ban: 6 → 14 категорий | [x] |
| 2.5.4 | Lessons learned 41-45, антипаттерны 21-22 | [x] |
| 2.5.5 | Бюджет, Quick Start, версия → v10 | [x] |
| 2.5.6 | DEVLOG + PLAN + ARCHITECTURE обновлены | [x] |

### Phase 3 — Запуски v10 [DONE]

Goal: прогонять пайплайн v10, накапливая гипотезы. Цель: подтвердить улучшение input quality.

| # | Task | Status |
|---|------|--------|
| 3.1 | Запуск v10 run 1 | [x] — 0 finalists, ~155K tokens, 25 searches. Rule Check 90% kill rate (Competition Pre-screen убил 11/13) |
| 3.2 | Сохранить артефакты + обновить results.md, DEVLOG | [x] — runs/v10-run1/ (4 файла) |
| 3.3 | Анализ: v10 vs v9 (freshness check effect, competition pre-screen effect) | [x] — см. ниже |
| 3.4 | Запуск v10 run 2 (Sonnet Competition Pre-screen) | [x] — 0 finalists, ~290K tokens, ~84 searches. Rule Check 65%, Critic 43%, Red Team 75%, QV 100%. Best: H6 WEAK (T2.5 demand) |

> v10 итого: 2 прогона, 0 финалистов. Competition Pre-screen Sonnet >> Haiku.
> Корневая проблема: Scout signal quality (T2-T3, нет T1/T1-alt potential).
> Решение: v11 (Phase 3.5).

### Phase 3.5 — v11: non-empty output + signal quality [DONE]

Goal: гарантировать непустой выхлоп каждого прогона + повысить качество Scout input.

| # | Task | Status |
|---|------|--------|
| 3.5.1 | Best Available carry-forward: лучший WEAK → Deep Validator (CONDITIONAL) | [x] |
| 3.5.2 | Scout Signal Quality Gate: >= 3 T1/T1-alt potential перед Generator | [x] |
| 3.5.3 | Quick Validator: T1-alt search для novel categories | [x] |
| 3.5.4 | Competition Pre-screen: Sonnet вместо Haiku | [x] |
| 3.5.5 | Lessons learned 46-48, антипаттерны 23-24 | [x] |
| 3.5.6 | Бюджет, Quick Start, версия → v11 | [x] |
| 3.5.7 | DEVLOG + PLAN + ARCHITECTURE обновлены | [x] |

### Phase 4 — Запуски v11 [DONE]

Goal: прогонять пайплайн v11, подтвердить непустой выхлоп и улучшение signal quality.

| # | Task | Status |
|---|------|--------|
| 4.1 | Запуск v11 run 1 | [x] — 1 WEAK (CONDITIONAL): H8 ClipDev (1.5/4 осей). Best Available activated. ~300K tokens, ~50 searches |

> v11 итого: 1 прогон, 1 WEAK (CONDITIONAL). Best Available сработал — выхлоп не пустой.
> Корневая проблема: transformation gap — Scout находит реальный сигнал, Generator придумывает differentiator, Validator не может подтвердить.
> Решение: v12 (Phase 4.5).

### Phase 4.5 — v12: evidence grounding [DONE]

Goal: устранить transformation gap — привязать Generator output к Scout evidence.

| # | Task | Status |
|---|------|--------|
| 4.5.1 | Spot-check validation (R0.75): 2 поиска на лучшие сигналы перед Generator | [x] |
| 4.5.2 | Scout-C depth pass (R0.75): 3 поиска x 3-5 лучших сигналов | [x] |
| 4.5.3 | Generator Evidence Anchor (правило 12): GROUNDED/SPECULATIVE маркировка | [x] |
| 4.5.4 | Lessons learned 49-54, антипаттерны 25-27 | [x] |
| 4.5.5 | Бюджет, Quick Start, версия → v12 | [x] |
| 4.5.6 | DEVLOG + PLAN + ARCHITECTURE обновлены | [x] |

### Phase 5 — Запуски v12 [FUTURE]

Goal: прогонять пайплайн v12, подтвердить evidence grounding и достижение MODERATE+.

| # | Task | Status |
|---|------|--------|
| 5.1 | Запуск v12 run 1 | [x] — 1 WEAK (CONDITIONAL): H7 InvoiceChase (2/4 осей). Best Available activated. ~391K tokens, ~182 searches |

### Phase 6 — Второй фреймворк [FUTURE]

Goal: построить отдельный фреймворк для второго этапа валидации накопленных гипотез.

> Не начинать до накопления ~100 гипотез. Это будет отдельный проект.
