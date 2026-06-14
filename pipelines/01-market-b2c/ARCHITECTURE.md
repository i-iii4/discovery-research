# Architecture: b2c-discovery

Related documents: [PLAN.md](PLAN.md) | [DEVLOG.md](DEVLOG.md) | [CLAUDE.md](CLAUDE.md) | [methodology.md](methodology.md)

## Context

Solo-разработчику нужно найти B2C-продукт, который можно построить за 2 недели и монетизировать до $5K/мес. Ручной поиск идей субъективен (founder bias) и медленный. Пайплайн автоматизирует генерацию и отсев гипотез через цепочку LLM-агентов с веб-поиском.

Ключевое ограничение: LLM-агенты не имеют актуальных данных о рынке. Без веб-поиска генератор производит правдоподобные, но незаземлённые гипотезы (v3-v4: 0 STRONG). Скауты решают эту проблему, подавая live demand signals.

## Pipeline (v12)

```
                    ┌──────────┐
                    │   LEAD   │  orchestrator (человек + Claude Code)
                    └────┬─────┘
                         │
   ┌─────────────────────┼──────────────────────────────────────────────┐
   │                     │                                              │
┌──┴───┐  ┌────────┐ ┌──┴──────┐  ┌──────────┐  ┌─────────┐  ┌─────────┐  │
│SCOUT │  │SCOUT-C │ │GENERATOR│  │ CRITIC   │  │QUICK VAL│  │DEEP VAL │  │
│A + B │→ │depth   │→│20 JTBD  │→ │2-3x mini │→ │blocker  │→ │demand+  │→ SYNTHESIS
│demand│  │pass    │ │evidence │  │web search│  │+ T1 scan│  │gap      │
│signal│  │3x5 srch│ │anchor   │  │2 per hyp │  │4 per hyp│  │10-15 sr │
└──────┘  └────────┘ └─────────┘  └──────────┘  └─────────┘  └─────────┘
                        │
              ┌─────────┴──────────┐
              │ RULE CHECK + DEDUP │  Sonnet: blacklist, Pattern Cap,
              │                    │  Free Alt Pre-screen, Competition Pre-screen
              │ DEDUP + FIT        │  Lead: merge, founder-fit, API
              └────────────────────┘
```

## Stages

| # | Stage | Agent | Model | Searches | Purpose |
|---|-------|-------|-------|----------|---------|
| R0 | Scout | 2x parallel | Sonnet | 10-15 each (+freshness) | Live demand signals + freshness check (v10) |
| R0.5 | Signal Quality Gate | Lead manual | — | 0 | >= 3 T1/T1-alt potential? Перезапуск Scout если нет (v11) |
| R0.75 | Spot-check + Scout-C | Lead + Sonnet | — | 2 + 9-15 | Spot-check конвертируемости (v12) + depth pass для 3-5 лучших сигналов (v12) |
| R1 | Generator | 1x | Sonnet | 0 | 20 JTBD-гипотез с Evidence Anchor: GROUNDED/SPECULATIVE (v12) |
| R1.5 | Rule Check | Lead manual | Sonnet | 0-20 | Blacklist, Pattern Cap, Free Alt, Competition Pre-screen (v10, Sonnet v11) |
| R1.5b | Dedup+Fit | Lead | — | 0-3 | Merge дублей, founder-fit check, API pre-screen |
| R2 | Critic | 2-3x parallel | Sonnet | 2 each per hyp | Kill 60%+, job overlap check. 2 агента при <8 гипотез |
| R2.25 | Red Team | 1x | Sonnet | 1-2 per hyp | Structural risks (5 категорий). RED FLAG = 2+ HIGH |
| R2.5 | Quick Valid | 1x | Haiku/Sonnet | 4 per hyp | Blocker check + T1/T1-alt scan + App Store scan. T1-alt для novel categories (v11) |
| R2.75 | Best Available | Lead manual | — | 0 | Если 0 survivors — лучший WEAK → Deep Validator (CONDITIONAL) (v11) |
| R3 | Deep Valid | 1-2x parallel | Sonnet | 10-15 per hyp | Demand evidence, competition, distribution, pricing. RED FLAG skip rule. +CONDITIONAL (v11) |
| R4 | Synthesis | Lead | — | 0-10 | Финальные досье + WWNBT для CONDITIONAL (v11) |

## Data Flow

```
Scout signals (30) → Quality Gate(v11) → Spot-check(v12) → Scout-C depth(v12) → Generator (20, Evidence Anchor v12) → Rule Check (8-14) → Dedup (8-12) → Critic (4-8) → Red Team → Quick Valid (2-5) → Best Available(v11) → Deep Valid (1-4) → Synthesis (1-3)
     ↑                  ↑                 ↑                  ↑                      ↑                  ↑                                     ↑                          ↑              ↑                   ↑
     │                  │                 │                  │                      │                  │                                     │                          │              │                   │
 whitelist         >= 3 T1/T1-alt    convertibility    workaround depth      GROUNDED/            Pattern Cap                           job overlap                 T1-alt         CONDITIONAL         RED FLAG
 5 patterns        potential         2 searches        3 srch x 3-5 sig     SPECULATIVE          Free Alt Pre-screen                   check                       T1-alt(v11)    if 0 survivors      skip rule
 freshness(v10)                                                              Evidence Anchor      Competition(Sonnet,v11)
```

## Key Decisions

### Evidence Tiers (v7)

| Tier | Определение | Вес |
|------|------------|-----|
| T1 | Прямой запрос "wish X existed" 50+ upvotes | Наивысший |
| T1-alt | Workaround chain (3+ шагов), регулярно выполняемый, с evidence повторяемости | = T1 (для novel categories) |
| T1.5 | Поведенческий сигнал 100+ upvotes, или конкурент 10K+ downloads < 4.0 rating | 2x T1.5 = 1x T1 |
| T2 | Жалоба на конкурента, 1-2 star review | Средний |
| T3 | Статья, исследование, обзор рынка | Низший |

### Scout Signal Priority (v9) + Freshness Check (v10)

WORKAROUND > EMERGING > UNDERSERVED > MISSING_FEATURE

> Scout-B: PRICING_GAP запрещён (v9). PH-сигналы допустимы только как EMERGING, не как DEMAND.
> Freshness check (v10): сигналы старше 6 мес проверяются доп. поиском на актуальность.

### Kill Rules (v7)

- 3+ конкурентов с рейтингом 4+, закрывающих ТОТ ЖЕ job → auto-KILL
- FREE tool с 100K+ users: job overlap HIGH → KILL, PARTIAL → WEAK, LOW → ALIVE
- Оба поиска Critic вернули 0 результатов → KILL
- API Dependency: HIGH + закрытый API → KILL
- Red Team: 2+ HIGH severity flags → RED FLAG (Lead решает)

### Final Verdict Scale

| Verdict | Criteria |
|---------|----------|
| STRONG | Demand (T1 или 2x T1.5) + clear gap + distribution + pricing |
| MODERATE | 3 из 4 осей |
| WEAK | 2 из 4 |
| KILL | < 2 |

## Performance History

| Version | Signals | Generated | After Critic | Final | Searches | Tokens |
|---------|---------|-----------|-------------|-------|----------|--------|
| v1 | — | 8 | 0 | 0 | ~60 | — |
| v2 | — | 25 | 7 | 2S+1M | ~40 | ~230K |
| v3 | — | 15 | 4 | 2M | ~64 | ~210K |
| v4 | — | 11 | 5 | 2M | ~80 | ~190K |
| v5 | 40 | 17 | 5 | 1M | ~176 | ~349K |
| v6 | 36 | 14 | 5 | 3M | ~113 | ~310K |
| v7-run1 | 37 | 19 | 3 | 1M | ~67 | — |
| v7-run2 | 37* | 18 | 2 | 0 | ~74 | — |
| v8-run1 | 34 | 12** | 2 | 2M | ~93 | ~300K |
| v9-run3 | 30 | 10** | 2 | 1S | ~80 | ~480K |
| v9-run7 | 25 | 7** | 0 | 0 | ~34 | ~263K |
| v10-run1 | 17 | 2*** | 0 | 0 | ~25 | ~155K |
| v10-run2 | 16 | 7*** | 4W | 0 | ~84 | ~290K |
| v11-run1 | 36 | 6**** | 2W | 1W(C) | ~50 | ~300K |

\* Сигналы переиспользованы из run 1. \*\* После Rule Check + Dedup. \*\*\* После Rule Check с Competition Pre-screen (v10). \*\*\*\* После Rule Check (v11: Signal Quality Gate + Competition Pre-screen Sonnet). W(C) = WEAK CONDITIONAL (Best Available Carry-Forward).
