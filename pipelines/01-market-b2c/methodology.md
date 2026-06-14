---
date: 2026-02-13
type: methodology
tags:
  - product-discovery
  - multi-agent
  - b2c
  - pet-project
  - methodology
  - jtbd
version: 12
---

# B2C Pet-Project Discovery v12

> Методология мультиагентного поиска B2C-продуктов для solo-разработчика.
> Фокус: одна функция, 2 недели до MVP, дистрибуция без маркетингового бюджета.
> Runtime: Claude Code (Task tool, `subagent_type="general-purpose"`).

**Эволюция подхода:**

| v1: Search-first | v2: Scout+Generate | v3-v4: Blind generate | v5-v9: Hybrid | v10: Quality-first | v11: Non-empty output | v12: Evidence grounding |
|---|---|---|---|---|---|---|
| Ищем боли в категориях | Scout-ы → Generator | Generator без внешних данных | Scout → Generate → Critic | Freshness check + Competition pre-screen | Best Available carry-forward | Scout depth + evidence anchor |
| Зрелые рынки = 0 ALIVE | Реальные цитаты = 2 STRONG | Training data = 0 STRONG | Demand signals + web-grounded | Input quality > filter quality | Signal quality gate + novel category T1-alt | Generator features привязаны к evidence |
| Research — bottleneck | Research для 3-5 выживших | Critic форсированно ищет | + Quick Validator gate | Scout проверяет свежесть сигналов | Каждый прогон = минимум 1 досье | Spot-check + Scout-C depth pass |
| **0 ALIVE из 8** | **2 STRONG из 25** | **0 STRONG, 4 MODERATE** | **1 STRONG из 7 прогонов v9** | **0 из 2 прогонов** | **1 WEAK(C) из 1** | **Target: >= 1 MODERATE** |

**Фактические результаты:**

| Run | Pipeline | STRONG | MODERATE | Critic searches | Total searches |
|-----|----------|--------|----------|-----------------|----------------|
| v1 | Search-first | 0 | 0 | 0 | ~60 |
| v2 | Scout+Generate | **2** | 1 | 0 | ~40 |
| v3 | Strict generate | 0 | 2 | 0 | ~64 |
| v4 | 2-phase Critic | 0 | 2 | **22** | **~80** |

**Что нового в v12 (vs v11):**
- **Scout-C depth pass** — после Signal Quality Gate Lead выбирает 3-5 лучших T1/T1-alt сигналов и запускает Scout-C (Sonnet, ~15 поисков): 3 поиска на сигнал для углубления workaround chain (шаги, цитаты, upvotes). v11-run1: Scout нашёл "developer clipboard underserved", но Generator придумал "auto-tag by IDE" — feature без evidence. Scout-C даёт Generator конкретный материал вместо абстракций
- **Generator Evidence Anchor (правило 12)** — core differentiator гипотезы ОБЯЗАН быть найден в demand signal. Если Generator добавляет feature из reasoning — помечает SPECULATIVE с confidence: LOW. v11-run1: 23 поиска — 0 evidence для "auto-tag by IDE project" (Generator hallucination)
- **Spot-check validation** — перед Generator Lead делает 2 поиска по 2 лучшим T1/T1-alt сигналам: "[exact job] wish there was" / "[exact workaround] better way". Если оба = 0 → сигналы мёртвые, перезапуск Scout. ~2K, дешевле пустого прогона ($1-2)

**Что нового в v11 (vs v10):**
- **Best Available carry-forward** — если после Quick Validator 0 survivors, лучшая WEAK-гипотеза автоматически идёт в Deep Validator с тегом CONDITIONAL. Synthesis пишет полное досье с вердиктом WEAK и секцией "What Would Need to Be True". v10: 2 прогона, 0 финалистов, ~$3 без выхлопа
- **Scout Signal Quality Gate** — перед Generator Lead проверяет: >= 3 сигнала с T1/T1-alt potential? Если нет — перезапуск одного Scout с уточнёнными запросами. v10: Scout находил T2-T3, Generator строил на них гипотезы, Critic не находил T1 — предсказуемый 0
- **Evidence tier calibration для novel categories** — Quick Validator ищет T1-alt (workaround chains) вместо T1 (wish posts) для гипотез в novel categories (anti-pattern, personal memory). Люди не просят продукт, которого не могут представить
- **Competition Pre-screen: Sonnet вместо Haiku** — v10-run1 (Haiku) дал 90% kill rate с false positives. v10-run2 (Sonnet) дал 65% — более точная оценка job overlap

**Что нового в v10 (vs v9):**
- **Scout freshness check** — для каждого сигнала старше 6 месяцев Scout делает 1 доп. поиск: "[problem] solution 2025 2026". Если решение уже существует — сигнал удаляется. v9-run7: 100% kill rate из-за устаревших сигналов (Pocket Casts добавил клипы, Monarch Extension закрыл Amazon боль, 5+ альтернатив заменили Chartable)
- **Competition Pre-screen в Rule Check** — Lead делает 1 поиск на гипотезу: "[product name] app". Если 3+ конкурента с 4+ рейтингом → KILL до Critic. v9-run7: Critic потратил ~77K, чтобы найти Screenotate, CLZ Books, Pocket Casts — 1 поиск нашёл бы их за 0 токенов
- **Расширенный Saturated Market Ban** — добавлены 8 категорий, стабильно убиваемых в v9: meal planning, tab management, gym tracking, meditation/relaxation, content scheduling, expense splitting, podcast analytics, read-it-later

**Что нового в v5 (vs v4):**
- **Round 0: Demand Scout** — 2 scout-агента ищут live demand signals (IH/Reddit/PH), Generator получает реальные цитаты вместо training data. Главное изменение — возвращает v2's grounding.
- **Generator: новые поля** — "Alternative Explanation" (защита от misdiagnosis, как H13 в v4), "API Dependency" (ранний detection блокеров, как H4 в v4)
- **Pattern cap** — max 4 гипотезы на один whitelist-паттерн (v4 произвёл 9/25 "personal memory")
- **API Pre-screen в Round 1.5** — 1 поиск на API-dependent гипотезу (сэкономил бы ~30 searches на H4)
- **Harder Critic kill** — 3+ конкурента с 4+ rating = auto-KILL. Kill rate v4 = 45% < target 60%
- **Round 2.5: Quick Validator** — Haiku, 3 searches per hypothesis. Blocker check + T1 scan перед дорогим Deep Validator
- **Validator: blocker-first** — сначала проверяет API access / platform restrictions, потом demand
- **Enriched blacklist** — не просто "cleaning audit trail", а "Turno $8/mo, Cleanster, 5+ competitors"

**Отличия от [[Multi-Agent Product Discovery]] (B2B):**

| B2B SaaS Discovery | B2C Pet-Project Discovery |
|---|---|
| Founder-market fit в конкретной индустрии | Founder-skill fit (что умею строить быстро) |
| TAM/SAM/SOM, отраслевые отчёты | Downloads лидера категории, keyword demand |
| Enterprise sales, conferences, LinkedIn | App Store, SEO, Product Hunt, viral, word-of-mouth |
| 3-6 месяцев до MVP | 2 недели до MVP |
| 10-20 B2B клиентов для $10K MRR | 500-2000 B2C пользователей для $5K MRR |

---

## Профиль основателя (заполнить перед запуском)

```
- Стек: [языки, фреймворки — что позволяет шипнуть за 2 недели]
- Режим работы: [вечера/выходные или full-time на проект]
- Интересные области: [не "в чём эксперт", а "что не вызывает отвращения"]
- Anti-области: [откуда хочет уйти, что точно НЕ строить]
- Целевой доход: [$X/мес]
```

> **Платформа не указана намеренно.** Код — коммодити. Платформа выбирается
> под задачу (job), а не наоборот. Один и тот же job может требовать
> extension, mobile app или CLI — это решается после выбора идеи.

> **"Scratch your own itch" убран намеренно.** Работает только когда
> личный профиль использования массовый. Если он нишевый — личные боли
> плохой рыночный сигнал. Ищем спрос через market-pull.

---

## Архитектура

### Подход: JTBD Intersection Generator

Вместо поиска проблем в известных категориях — генерация гипотез на пересечениях.

**Формула:**
```
[Кто — конкретный человек] + [Ситуация — когда/где] + [Ограничение — что мешает]
= Underserved Job
```

**Примеры пересечений:**
- Фрилансер + переключается между 5 клиентами + путает контексты = job: мгновенное переключение рабочего контекста
- Родитель + ребёнок с хроническим заболеванием + приём врача через неделю = job: быстрая фиксация симптомов для отчёта
- Студент + готовится к экзамену + не понимает что именно не знает = job: выявление gaps в знаниях

### Роли (7-9 агентов + Lead)

```
                              ┌─────────────┐
                              │  LEAD       │  orchestrator + synthesizer
                              │  (ты сам)   │  решает, мержит, пишет отчёт
                              └──────┬──────┘
                                     │
  ┌──────────┬──────────┬────────┬───┴────┬────────────┬────────────────┐
  │          │          │        │        │            │                │
┌─┴──────┐ ┌┴────────┐ ┌┴──────┐ ┌┴──────┐ ┌┴───────────┐ ┌┴─────────────┐
│ SCOUT  │ │GENERATOR│ │RULE   │ │CRITIC │ │QUICK VALID.│ │DEEP VALID.   │
│ 2 агент│ │ 20 JTBD │ │CHECK  │ │2-3   │ │ Haiku      │ │ 1-2 Sonnet   │
│ demand │ │(+signal)│ │Sonnet │ │мини   │ │ 4 searches │ │ 10+ searches │
│ signals│ │         │ │0-12   │ │job    │ │ +App Store │ │ RED FLAG skip│
│        │ │         │ │srch   │ │overlap│ │            │ │              │
└────────┘ └─────────┘ └───────┘ └───────┘ └────────────┘ └──────────────┘
                                    ┌────────────┐
                                    │ RED TEAM   │
                                    │ 1 Sonnet   │
                                    │ devil's    │
                                    │ advocate   │
                                    └────────────┘
```

#### SCOUT (Demand Scout) — NEW в v5, обновлён в v12
- **Задача:** найти 20-30 live demand signals из IH/Reddit/PH/App Store
- **Метод:** web search по шаблонам ("wish there was", "looking for alternative", etc.)
- **Выход:** цитаты с URL, upvotes, датой — конкретные фразы реальных людей
- **Freshness check (v10):** для сигналов старше 6 мес — 1 доп. поиск на актуальность
- **Scout-C depth pass (v12):** для 3-5 лучших T1/T1-alt сигналов — 3 доп. поиска на каждый для углубления workaround chain
- **Почему:** v2 (со scout-ами) дал 2 STRONG, v3-v4 (без scout-ов) дали 0 STRONG. Generator нужны реальные данные. v11-run1: breadth-first signals → Generator hallucinated features.

#### GENERATOR (Генератор гипотез)
- **Задача:** 20 JTBD-гипотез на пересечениях ниш
- **Input:** demand signals от Scout + blacklist/whitelist + профиль основателя
- **Метод:** рассуждение, заземлённое в реальных цитатах от Scout
- **Формула:** [Кто] + [Ситуация] + [Ограничение] = Job → Product hypothesis
- **Новые поля:** "Alternative Explanation" + "API Dependency"
- **Ограничение:** max 4 гипотезы на один whitelist-паттерн

#### CRITIC (2-3 параллельных мини-агента)
- **Метод:** 2 агента (при <8 гипотез) или 3 (при 8+), 2 web search на гипотезу
- **KPI:** убить минимум 60%. Job overlap check вместо бинарного kill
- **Вердикт:** KILL / WEAK / ALIVE + Confidence: HIGH / LOW
- **Проверено v4:** 3 мини-агента сделали 22 web search (vs 0 в v2/v3)

#### RED TEAM (Devil's Advocate) — NEW в v7
- **Задача:** найти причины провала КРОМЕ конкуренции для каждой выжившей гипотезы
- **Модель:** Sonnet (нужен reasoning)
- **Метод:** 1-2 web search на гипотезу по специфическим рискам
- **Input:** ALIVE + WEAK гипотезы после Critic
- **Выход:** для каждой гипотезы — 0-3 structural risks с severity (LOW/MEDIUM/HIGH)
- **Не убивает:** только добавляет risk flags. Решение принимает Lead или Quick Validator

#### QUICK VALIDATOR (Gate) — NEW в v5, обновлён в v8
- **Задача:** быстрая проверка перед дорогим Deep Validation
- **Модель:** Haiku (дешёвый, быстрый)
- **Метод:** 4 web search на гипотезу: 1) blocker check, 2) T1 scan, 3) competition scan, 4) App Store scan
- **Выход:** PASS (→ Deep Validator) / BLOCK (→ KILL с причиной) / NO_SIGNAL (→ KILL)

#### DEEP VALIDATOR (Проверщик спроса)
- **Задача:** для 3-6 прошедших Quick Validator — глубокая проверка demand + distribution
- **Метод:** web search по шаблонам, App Store data, Reddit evidence, pricing benchmarks
- **Strategy:** blocker-first (проверяет API/platform access ДО demand research)
- **Выход:** полное досье с evidence tiers (T1/T1.5/T2/T3)

---

## Фазы (5 раундов + синтез)

### Раунд 0: Demand Scout — NEW в v5
**Цель:** 20-30 live demand signals из реальных сообществ
**Время:** ~10-15 мин (2 агента параллельно)
**Токены:** ~30-50K (2 Sonnet)
**Работают:** 2 SCOUT-а параллельно
**Web search:** ДА, 10-15 запросов на агента

> **Почему:** v2 (со скаутами) дал 2 STRONG, v3-v4 (без скаутов) дали 0 STRONG.
> Generator, работающий только на training data, производит правдоподобные,
> но незаземлённые гипотезы. Скауты дают ему реальные цитаты и URL-ы.

> **Это рандомайзер — и это ОК.** Scout не выбирает лучшие ниши — он собирает
> случайную выборку live demand signals. Но даже случайная выборка из РЕАЛЬНЫХ
> данных лучше, чем генерация из training data. Сигналы от Scout — это seed,
> а не filter.

---

**Промпт для Scout-A (IH/Reddit/Discord):**

```
Ты — demand scout. Твоя задача — найти 15-20 живых сигналов спроса
от реальных людей в интернете. Ищи НА АНГЛИЙСКОМ.

## Профиль основателя
[ВСТАВИТЬ ИЗ СЕКЦИИ ВЫШЕ]

## Whitelist-паттерны (приоритет)
[ВСТАВИТЬ ИЗ CROSS-RUN LEARNING]

## Метод: поиск demand signals

Сделай 10-15 web search запросов по шаблонам:

### Шаблоны запросов:
1. "reddit [whitelist-паттерн] wish there was"
2. "indie hackers looking for [whitelist-topic] tool"
3. "reddit [persona] frustrated with [tool category]"
4. "hacker news ask hn [problem domain]"
5. "[competitor] alternative reddit [year]"
6. "reddit is there an app that [job description]"
7. "discord [whitelist-topic] looking for tool"

### Для каждого найденного сигнала запиши:
- **URL** (обязательно)
- **Цитата** (точная фраза, 1-2 предложения)
- **Автор/контекст** (кто пишет — freelancer, parent, student, etc.)
- **Engagement** (upvotes, comments)
- **Дата** (год)
- **Signal type:** WISH (хочет продукт), PAIN (описывает боль),
  COMPLAINT (жалуется на существующее), WORKAROUND (построил руками)

### Правила:
- НЕ используй site:reddit.com — ищи "reddit [topic]"
- Приоритет: WISH и WORKAROUND > PAIN > COMPLAINT
- Минимум 15 сигналов, из минимум 8 разных доменов
- WORKAROUND — самый сильный сигнал (человек УЖЕ строит решение руками)
- Не возвращай общие статьи — только конкретные запросы/жалобы реальных людей

### Freshness check (NEW v10):
Для каждого сигнала, у которого дата старше 6 месяцев:
- Сделай 1 доп. web search: "[problem description] solution 2025 2026"
- Если нашёл продукт, который УЖЕ решает эту проблему → УДАЛИ сигнал
- Если продукт не найден → оставь, пометь "freshness: checked"
- Цель: не передавать Generator устаревшие боли, уже закрытые рынком

> **v9-run7 lesson:** Scout нашёл "podcast clip sharing frustration" (2024),
> но Pocket Casts уже добавил clip sharing. "Amazon line items pain" (2025),
> но Monarch Extension уже закрыл проблему. 100% kill rate в Critic —
> все 7 гипотез были в уже решённых нишах.

Верни список из 15-20 demand signals в формате выше.
```

**Промпт для Scout-B (HN/AppStore/Discord):**

```
Ты — demand scout. Твоя задача — найти 15-20 живых сигналов спроса
через Hacker News, App Store reviews, Discord communities и alternative-seeking.
Ищи НА АНГЛИЙСКОМ.

## Профиль основателя
[ВСТАВИТЬ ИЗ СЕКЦИИ ВЫШЕ]

## Whitelist-паттерны (приоритет)
[ВСТАВИТЬ ИЗ CROSS-RUN LEARNING]

## Метод: поиск через продукты и отзывы

Сделай 10-15 web search запросов по шаблонам:

### Шаблоны запросов:
1. "hacker news show hn [whitelist-topic] side project"
2. "reddit built my own solution for [whitelist-topic]"
3. "[popular tool] workaround reddit how to"
4. "app store [category] missing feature reviews"
5. "discord [whitelist-topic] community tool request"
6. "[tool] vs [tool] reddit which is better [year]"
7. "product hunt [whitelist-topic] launched 2025 2026"

### Для каждого найденного сигнала запиши:
- **URL** (обязательно)
- **Цитата** (точная фраза)
- **Контекст** (откуда: PH comment, App Store review, Reddit, HN)
- **Engagement** (upvotes, rating)
- **Дата**
- **Signal type:** WORKAROUND (построил сам), EMERGING (новый side project),
  UNDERSERVED (аудитория не обслуживается), MISSING_FEATURE (нет нужного)

### Правила:
- **НЕТ PRICING_GAP.** Не возвращай ценовые жалобы ("too expensive",
  "cheaper alternative"). Scout-A уже ловит complaints — дублировать не нужно.
  PRICING_GAP ведёт в red ocean, где бесплатные альтернативы убивают гипотезы.
- Приоритет: WORKAROUND > EMERGING > UNDERSERVED > MISSING_FEATURE
- Минимум 10 сигналов, из минимум 6 разных доменов
- PH-сигналы допустимы только как EMERGING (новый side project < 6 мес),
  НЕ как DEMAND. PH upvotes — это enthusiasm, не purchase intent
- Не возвращай general reviews — только конкретные gaps и complaints

### Freshness check (NEW v10):
Для каждого сигнала, у которого дата старше 6 месяцев:
- Сделай 1 доп. web search: "[problem description] solution 2025 2026"
- Если нашёл продукт, который УЖЕ решает эту проблему → УДАЛИ сигнал
- Если продукт не найден → оставь, пометь "freshness: checked"

> **v5 lesson:** Scout-B с приоритетом PRICING_GAP нашёл 14/20 pricing gaps →
> Generator создал гипотезы в red ocean → Critic убил 71%.
> **v8 lesson:** несмотря на правило "PRICING_GAP только если free не найден",
> Scout-B снова выдал 8/20 (40%) PRICING_GAP. Промптовое ограничение не работает —
> PRICING_GAP полностью убран из Scout-B. Scout-A ловит ценовые жалобы в формате
> COMPLAINT, этого достаточно.

Верни список из 10-15 demand signals в формате выше.
```

---

#### Scout Signal Quality Gate (NEW v11, обновлён в v12)

Перед Generator — Lead проверяет качество сигналов:

1. **Посчитать T1/T1-alt potential:** сколько сигналов содержат прямой wish
   с 50+ upvotes (T1) или описанный workaround chain 3+ шагов (T1-alt)?
2. **Минимальный порог:** >= 3 сигнала с T1/T1-alt potential
3. **Если порог не пройден:**
   - Определить, какие whitelist-паттерны недопредставлены
   - Перезапустить одного Scout-а с уточнёнными запросами:
     "reddit [underrepresented pattern] workaround step by step"
   - Не перезапускать обоих — один Scout + существующие сигналы достаточно
4. **Если порог пройден:** Spot-check validation (шаг 5), затем Scout-C (шаг 6)

#### Spot-check Validation (NEW v12)

5. **Spot-check:** Lead делает 2 web search по 2 лучшим T1/T1-alt сигналам:
   - `"reddit [exact job from signal] wish there was"` или
   - `"reddit [exact workaround from signal] better way"`
   - Если оба = 0 результатов → сигналы "мёртвые" (потенциал есть,
     но evidence не конвертируется). Перезапуск одного Scout-а.
   - Если хотя бы 1 вернул результат → PASS, перейти к Scout-C.
   - **Бюджет:** 2 поиска, ~2K токенов.

> **Зачем:** v11-run1 Quality Gate прошёл (14/16 T1/T1-alt potential), но при
> валидации 23 поиска за core differentiator = 0 evidence. Gate проверял
> *потенциал*, а Spot-check проверяет *конвертируемость*. 2 поиска за ~2K —
> дешевле пустого прогона ($1-2).

#### Scout-C Depth Pass (NEW v12)

6. **Scout-C:** Lead выбирает 3-5 лучших T1/T1-alt сигналов и запускает
   Scout-C (Sonnet) с заданием: для каждого сигнала — 3 доп. поиска:
   - `"reddit [exact workaround from signal] how to step by step"`
   - `"reddit [exact workaround] alternative better way"`
   - `"[exact tool mentioned in workaround] complaints limitations"`

**Промпт для Scout-C:**

```
Ты — depth scout. Твоя задача — УГЛУБИТЬ уже найденные demand signals.
НЕ ищи новые сигналы. Ищи ДЕТАЛИ по существующим.

## Сигналы для углубления (3-5 штук)
[ВСТАВИТЬ ЛУЧШИЕ T1/T1-alt СИГНАЛЫ ОТ SCOUT-A/B]

## Для КАЖДОГО сигнала сделай 3 web search:

1. "[exact workaround from signal] how to step by step reddit"
   — Ищешь: конкретные шаги workaround (сколько шагов? сколько времени?
   как часто повторяют? какие инструменты используют?)

2. "[exact workaround] alternative better way reddit"
   — Ищешь: пробовали ли люди другие решения? что не устроило?
   какие gaps остались?

3. "[tool mentioned in workaround] complaints limitations [year]"
   — Ищешь: конкретные жалобы на текущее решение. Рейтинги, отзывы,
   upvoted complaints.

## Для каждого результата запиши:
- **URL** (обязательно)
- **Цитата** (точная фраза, включая workaround steps)
- **Engagement** (upvotes, comments)
- **Workaround chain:** [шаг 1] → [шаг 2] → [шаг 3] → ...
  (конкретные действия, инструменты, время на каждый шаг)
- **Gap:** что workaround НЕ решает? (потеря данных, время, friction)

## Правила:
- НЕ ищи новые сигналы — только углубляй существующие
- Приоритет: конкретные workaround steps > общие жалобы
- Если поиск вернул 0 — так и пиши, не придумывай
- Минимум 2 URL на сигнал (из 3 поисков)
```

**Выход Scout-C:** для каждого из 3-5 сигналов — enriched version:
- Workaround chain с конкретными шагами и инструментами
- Gaps в workaround (что не решает)
- Дополнительные цитаты с upvotes
- Жалобы на текущие инструменты

**Бюджет:** ~15-20K, 9-15 поисков. Generator получает конкретный материал
для features вместо абстрактных сигналов.

> **Зачем:** v2 (2 STRONG) получал от Scout-ов конкретные цитаты типа
> "wish there was a cheaper Canny" — и Generator строил на них Feature Memory.
> v11-run1 Scout нашёл "developer clipboard underserved" (абстрактно),
> Generator придумал "auto-tag by IDE project" (из reasoning), Validator
> не нашёл evidence (0 из 23 поисков). Scout-C превращает абстрактные
> сигналы в конкретные workaround chains — Generator строит features
> на evidence, а не на hallucination.

**Зачем Signal Quality Gate (v11):** v10-run1 и v10-run2 дали 0 финалистов.
Корневая причина — Scout нашёл сигналы уровня T2-T3 (статьи, жалобы),
Generator построил на них гипотезы, Critic/Quick Validator искали T1 evidence
и не нашли. Проверка качества сигналов ДО Generator предотвращает прогон
на заведомо слабом input.

> **v10 lesson:** v10-run2 лучший сигнал = T2.5 (статьи + Etsy шаблоны).
> Ни один сигнал не имел T1/T1-alt potential. Generator не может компенсировать
> слабый input — он комбинирует сигналы, а не создаёт спрос.

---

### Раунд 1: Generate
**Цель:** 20-30 JTBD-гипотез на пересечениях ниш, заземлённых в demand signals
**Время:** ~15-20 мин
**Токены:** ~40-60K (1 агент + Lead)
**Работают:** LEAD формулирует задание, GENERATOR генерирует
**Web search:** НЕТ. Рассуждение на основе demand signals от Scout.

---

**Промпт для Generator-а:**

```
Ты — генератор продуктовых гипотез. Твоя задача — найти UNDERSERVED JOBS
на пересечениях ниш. НЕ ищи в интернете. Используй demand signals от Scout-ов
и свои знания о людях, их ситуациях и ограничениях.

## Профиль основателя
[ВСТАВИТЬ ИЗ СЕКЦИИ ВЫШЕ]

## Demand Signals от Scout-ов
[ВСТАВИТЬ 30-40 СИГНАЛОВ ОТ SCOUT-A И SCOUT-B]

## Метод: JTBD Intersection

Формула: [Кто] + [Ситуация] + [Ограничение] = Underserved Job → Product

ВАЖНО: используй demand signals как SEED для генерации.
Каждая гипотеза должна быть СВЯЗАНА хотя бы с одним сигналом.
Можешь комбинировать несколько сигналов в одну гипотезу.
Можешь развивать сигнал в неожиданном направлении.
НО: не игнорируй сигналы — они из реального мира.

### Шаг 1: Персоны (минимум 10)
Выпиши 10+ типов людей, которые:
- Используют цифровые инструменты ежедневно
- Готовы платить за решение бытовых/рабочих проблем
- Не обслуживаются enterprise-софтом

Примеры: фрилансер-дизайнер, родитель ребёнка с аллергией, студент-медик,
remote worker в другом часовом поясе, контент-креатор на YouTube,
человек на кето-диете, junior developer на испытательном сроке...
НЕ использовать: ADHD/neurodivergent-персоны (blacklist #15).

### Шаг 2: Ситуации (минимум 10)
Для каждой персоны — 2-3 специфические ситуации,
в которых существующие инструменты НЕ работают.
Ситуация = момент + контекст + эмоция.

Примеры: утро понедельника с 20 непрочитанными письмами,
переключение между личным и рабочим контекстом,
поиск "того самого видео" которое видел неделю назад...

### Шаг 3: Ограничения (минимум 8)
Что делает существующие решения непригодными:
- Время: "у меня 2 минуты, не 20"
- Когнитивная нагрузка: "я и так перегружен"
- Приватность: "не хочу отдавать данные"
- Цена: "не буду платить $20/мес за одну функцию"
- Платформа: "мне нужно это на телефоне в метро"
- Контекст: "я в потоке, не хочу переключаться"
- Социальность: "мне неловко просить/спрашивать"
- Доверие: "не доверяю AI с моими данными"

### Шаг 3.5: Goal Graph (AJTBD)

Для каждого demand signal построй мини-граф целей из 3 уровней:

1. **Предыдущая работа** — что клиент делает ДО столкновения с болью?
   Где он находится за шаг до проблемы? Здесь конкурентов меньше всего.
   Пример: "найти квартиру" → предыдущая: "понять, что могу себе позволить"

2. **Очевидная работа** — то, что signal описывает напрямую.
   ⚠️ ВНИМАНИЕ: здесь МАКСИМУМ конкурентов. Это уровень лобовой атаки.
   Пример: "задокументировать квартиру при заселении"

3. **Работа уровнем выше** — ради чего клиент это делает?
   Более абстрактная цель. Здесь возможен другой form-factor.
   Пример: "защитить свои деньги при аренде"

Также ищи **подцели для убийства** — обязательные промежуточные шаги,
которые можно устранить.
Пример: "чтобы осмотреть квартиру, надо позвонить, договориться, доехать"
→ убийство подцели: видео-тур вместо личного осмотра.

**ПРАВИЛО:** строй гипотезу НЕ на уровне 2 (очевидная работа), а на уровне
1 (предыдущая) или 3 (выше). Уровень 2 допустим ТОЛЬКО если:
- Конкурентов на этом уровне < 3 (т.е. рынок действительно пустой)
- Или у тебя есть уникальный form-factor/UX, недоступный конкурентам
Если строишь на уровне 2 — пометь **LEVEL_2_DIRECT** и обоснуй.

> **v12 lesson:** 3 прогона подряд Competition Pre-screen убивал 57-62%
> гипотез. Корневая причина: Generator шёл в лобовую атаку на очевидный
> job — туда, где 5+ конкурентов уже стоят. "Screenshot organizer" → 7
> конкурентов, "offline budget" → 8 конкурентов, "HN read tracker" → 6
> бесплатных расширений. Goal Graph заставляет искать менее очевидные
> (и менее занятые) точки в графе целей клиента.

### Шаг 4: Пересечения → Гипотезы (20 штук)

Комбинируй [Персона] + [Ситуация] + [Ограничение] = Job.
Используй Goal Graph: атакуй предыдущую работу или работу уровнем выше.
Для каждого job сформулируй продуктовую гипотезу:

```markdown
## H[N]: [Название продукта]
- **Job:** [Персона] + [Ситуация] + [Ограничение]
- **Job statement:** Когда я [ситуация], я хочу [действие],
  чтобы [результат]
- **Demand signal:** [ссылка на конкретный сигнал от Scout-а, который вдохновил эту гипотезу]
- **Продукт:** [одно предложение — что это делает]
- **Форм-фактор:** [web app / mobile / extension / CLI / desktop]
- **Почему сейчас:** [что изменилось, почему это не было решено раньше]
- **MVP scope:** [2-3 экрана/функции максимум]
- **Monetization signal:** [за что похожее люди уже платят]
- **Почему не существует:** [структурная причина — технология появилась недавно /
  рынок считался слишком маленьким / проблема незаметна извне / etc.]
- **Alternative Explanation:** [почему люди МОГУТ не хотеть этот продукт,
  даже если боль существует? Например: боль реальна, но решают иначе;
  или: поведение вызвано не тем, чем кажется (как ADHD app hopping =
  dopamine seeking, а не forgetting)]
- **API Dependency:** [NONE / LOW / HIGH — зависит ли MVP от закрытого API?
  Если HIGH — указать какой API и есть ли публичный доступ.
  Пример: "HIGH — Airbnb API invitation-only" = blocker]
- **Goal Graph Level:** [PREVIOUS / HIGHER / SUBGOAL_KILL / LEVEL_2_DIRECT]
  Какой уровень Goal Graph атакует гипотеза?
  - PREVIOUS — предыдущая работа (до столкновения с болью)
  - HIGHER — работа уровнем выше (ради чего)
  - SUBGOAL_KILL — убийство обязательной подцели
  - LEVEL_2_DIRECT — лобовая атака на очевидный job (нужно обоснование)
```

## Правила генерации

1. ЗАПРЕЩЕНО категорийное мышление:
   - НЕ "ещё один todo-app" → ДА "todo для контент-креаторов
     с 5 платформами и дедлайнами от брендов"
   - НЕ "AI калории" → ДА "фото-лог еды для человека
     с расстройством пищевого поведения, которому нельзя видеть цифры"

2. ЗАПРЕЩЕНО "AI wrapper for X" без конкретного job.
   AI может быть внутри, но job первичен.

3. Каждая гипотеза должна быть BUILDABLE за 2 недели одним разработчиком.
   Если требует датасет, ML training, или сложного backend — не подходит.

4. Каждая гипотеза должна иметь DISTRIBUTION STORY.
   "Где именно этот человек узнает об этом продукте?"

5. Приоритизируй пересечения, где:
   - Существующие решения СЛИШКОМ сложны для конкретного job
   - Целевая аудитория ПЛАТИТ за похожие инструменты
   - Есть КОНКРЕТНОЕ сообщество (subreddit, discord, forum)

6. DIVERSITY: максимум 2 гипотезы на одну персону.
   Минимум 12 РАЗНЫХ персон из 8+ доменов.
   Не кластеризуй всё в productivity. Покрой:
   health, creative work, learning, social, financial,
   и неожиданные пересечения.
   НО: для 3-5 лучших персон — дай 2 варианта продукта
   (разные форм-факторы или разные ситуации для одного job).
   Глубина > ширина для топовых идей.
   **ADHD/ND ЗАПРЕТ:** 0 гипотез с ADHD/neurodivergent-персонами.
   Категория в blacklist #15. Проблема реальна, но нет работающей
   методологии — целевая аудитория не может регулярно использовать
   приложения (executive dysfunction → retention провал).
   5 из 7 прогонов генерировали ADHD-финалистов, ни один не жизнеспособен.

7. CROSS-RUN LEARNING (если есть данные из предыдущих прогонов):
   [ВСТАВИТЬ BLACKLIST — паттерны убитых гипотез]
   [ВСТАВИТЬ WHITELIST — паттерны выживших гипотез]
   Не генерируй гипотезы с blacklist-паттернами.
   Приоритизируй whitelist-паттерны.
   **PATTERN CAP:** максимум 4 гипотезы на один whitelist-паттерн.
   v4 произвёл 9/25 "personal memory" — это кластеризация, не diversity.

8. DEMAND SIGNALS: каждая гипотеза должна ссылаться на конкретный
   demand signal от Scout-а. Если signal не подходит ни к одной гипотезе —
   всё равно включи его как поле "Demand signal" с пометкой "слабая связь".
   Гипотезы БЕЗ связи с demand signals допустимы (max 5 из 25),
   но помечаются как "UNSUPPORTED" — они первые кандидаты на kill.

9. FREE ALTERNATIVE CHECK: если гипотеза предполагает pricing gap
   ($X/mo vs дешевле), ОБОСНУЙ почему free альтернативы не закрывают job.
   Примеры СЛАБОГО reasoning (= LOW confidence):
   - "Free version limited" (без конкретики ЧТО ограничено и ПОЧЕМУ это важно)
   - "Free version has ads" (ads = weak moat, люди терпят)
   Примеры СИЛЬНОГО reasoning (= ok):
   - "Free plugin требует 30min manual setup, target audience = non-technical"
   - "Free tool desktop-only, job требует mobile контекст (в метро/магазине)"
   - "Free tool без conflict resolution, потеря данных = критично для PKM"
   Если не можешь обосновать → пометь гипотезу LOW confidence.

   > **v5 lesson:** Generator не учёл tawk.to (FREE 100%), Remotely Save
   > (FREE 100K+ downloads), Franz (FREE), Uptime Kuma (FREE self-hosted).
   > Critic убил все эти гипотезы. Generator должен сам проверять.

10. Для каждой гипотезы ответь: "ПОЧЕМУ ЭТО ЕЩЁ НЕ СУЩЕСТВУЕТ?"
    Если не можешь придумать причину — возможно, оно уже существует
    или рынок слишком мал. Добавь поле:
    - **Почему не существует:** [структурная причина]

11. SATURATED MARKET BAN: НЕ генерируй гипотезы в категориях, где
    ты знаешь о 5+ established players с 100K+ users или 4+ рейтингом.
    Примеры saturated: grammar checking (Grammarly/QuillBot/LanguageTool),
    time tracking (Toggl/Clockify/RescueTime), read-it-later (Instapaper/
    Readwise/Raindrop/Pocket), meeting transcription (Fireflies/Otter/Read.ai),
    personal CRM (Clay/Dex/Covve/Monica), sheets-to-email (Mailmeteor/YAMM),
    meal planning (Mealime/Paprika/Yummly/Eat This Much/Plan to Eat),
    tab management (OneTab/Workona/Toby/Session Buddy/Tab Wrangler),
    gym/workout tracking (Strong/JEFIT/Hevy/FitBod/GymBook),
    meditation/relaxation (Calm/Headspace/Insight Timer/Balance/Ten Percent),
    content scheduling (Buffer/Hootsuite/Later/Sprout Social/Publer),
    expense splitting (Splitwise/Tricount/Settle Up/Tab/IOU),
    podcast analytics (Spotify for Creators/Captivate/Podtrac/Chartable/Ausha),
    book cataloging (Goodreads/StoryGraph/Libib/CLZ Books/BookBuddy).
    Если demand signal указывает на такую категорию — ищи NOVEL ANGLE
    (новый form-factor, новая аудитория, новый UX), а не pricing gap.
    > **v9 lesson:** 5 из 7 прогонов v9 дали 0 финалистов. Корневая причина:
    > Generator генерировал в mature markets. v9-run7: 9/20 (45%) убиты
    > по saturated market — meal planning, tab management, gym tracking,
    > meditation, content scheduling, expense splitting, read-it-later.
    > **v10 fix:** расширен список с 6 до 14 категорий на основе данных v9.

12. **EVIDENCE ANCHOR (NEW v12):** core differentiator гипотезы ОБЯЗАН быть
    найден в demand signal от Scout-а (включая Scout-C depth pass).
    - Если differentiator = конкретная функция/UX из workaround chain Scout-а
      → пометь **GROUNDED** и укажи сигнал
    - Если differentiator придуман из reasoning (нет в сигналах)
      → пометь **SPECULATIVE** и поставь confidence: LOW
    - SPECULATIVE гипотезы допустимы (max 3 из 20), но они первые кандидаты
      на kill в Rule Check
    - **Примеры:**
      - Scout нашёл: "I forward invoices to spreadsheet manually" →
        Generator: "auto-parse invoice from email" = **GROUNDED** (из workaround)
      - Scout нашёл: "developer clipboard manager underserved" →
        Generator: "auto-tag clips by IDE project" = **SPECULATIVE** (из reasoning,
        никто не просил auto-tag by IDE)
    > **v11-run1 lesson:** Generator придумал "auto-tag clipboard by IDE project"
    > на основе абстрактного сигнала "developer clipboard underserved". 23 поиска
    > Deep Validator — 0 evidence что кто-то хочет эту feature. Core differentiator
    > = hallucination. Evidence Anchor заставляет Generator маркировать, что подтверждено
    > сигналами, а что — его гипотеза.

13. **GOAL GRAPH STRATEGY (NEW v13):** для каждой гипотезы укажи Goal Graph
    Level (PREVIOUS / HIGHER / SUBGOAL_KILL / LEVEL_2_DIRECT).
    - **LEVEL_2_DIRECT** (лобовая атака на очевидный job) — max 5 из 20.
      Остальные 15+ должны быть PREVIOUS, HIGHER или SUBGOAL_KILL.
    - Если LEVEL_2_DIRECT — обоснуй: почему конкурентов < 3 на этом уровне
      или какой уникальный form-factor делает тебя неуязвимым.
    - **Примеры:**
      - Signal: "арендаторы делают сотни фото квартиры"
        LEVEL_2_DIRECT: "app для фото квартиры" → 5+ конкурентов → KILL
        PREVIOUS: "помочь понять права арендатора ДО заселения" → меньше конкурентов
        HIGHER: "полная защита денег при аренде" → другой form-factor (юр.сервис)
        SUBGOAL_KILL: "автоматически найти фото через 2 года" → реальный gap
      - Signal: "offline budget without bank login"
        LEVEL_2_DIRECT: "offline budget app" → 8+ конкурентов → KILL
        PREVIOUS: "понять какой метод бюджетирования подходит мне" → quiz/onboarding
        HIGHER: "контроль над финансами без тревоги" → behavioral coaching
    > **v12 lesson:** Competition Pre-screen убивал 57-62% гипотез потому что
    > Generator атаковал очевидный job прямо в центр — где конкуренты уже стоят.
    > AJTBD Goal Graph — метод Замесина для побега из красного океана: зайти
    > через предыдущую работу (где конкурентов нет) или работу уровнем выше
    > (где form-factor другой).

Сгенерируй 20 гипотез. Пронумеруй H1-H20.

> **v9 change:** было 25. При 30 сигналах Scout и 15 blacklist-записях,
> 25 гипотез = натягивание. v8: 13/25 убиты на Dedup/founder-fit, до Critic
> доходит ~12. 20 гипотез = меньше мусора, экономия ~10K токенов.
```

---

### Раунд 1.5: Lead Dedup + Founder-Fit (между раундами)
**Цель:** убрать дубли и проверить founder-fit до отправки Critic-у
**Время:** ~2-5 мин
**Токены:** ~5K (Haiku) или 0 (вручную)
**Работает:** LEAD (рекомендуется) или DEDUP-агент (Haiku)

> **v9 lesson: Lead manual > Haiku.** В v9-run1 Haiku Rule Check потратил ~27K
> на reasoning и сделал 1 tool_use — Free Alt Pre-screen выполнен Lead вручную.
> В v9-run2 Lead сделал весь Rule Check вручную: надёжнее (поймал ChatGPT Memory
> и Ollama+Open WebUI), дешевле (0 токенов агента), быстрее (5 мин vs 10 мин Haiku).
> **Рекомендация: Rule Check + Dedup + Founder-Fit — Lead вручную.**

**Вариант A — автоматический (рекомендуется):**

Запустить агент (Haiku, дешёвый) с промптом:
```
Вот [N] JTBD-гипотез и профиль основателя.

## Профиль основателя
[ВСТАВИТЬ]

## Задачи

### 1. Дедупликация
Найди группы гипотез с одной целевой аудиторией И похожим продуктом.
Для каждой группы — предложи merge (какую оставить, что взять из других).
Критерий: если два продукта решают один job для одних людей — это дубль.

### 2. Founder-fit
Для каждой гипотезы — founder-fit score (1-5):
- 5: Основатель в этой аудитории сам / горит темой
- 4: Интересно, готов изучать
- 3: Нейтрально, но не отталкивает
- 2: Чуждо, но технически интересно
- 1: Категорически чуждо

Если score < 2 — предложи KILL с объяснением.

### Выход
Таблица: | # | Гипотеза | Merge? | Founder-fit (1-5) | Решение (KEEP/MERGE/KILL) |
```

Lead просматривает таблицу, подтверждает или корректирует решения.

**Вариант B — ручной:**

Lead делает две вещи:

**1. Дедупликация:**
Прочитать все гипотезы и найти пары/группы с одной и той же целевой аудиторией
и похожим продуктом. Мержить в одну гипотезу, взяв лучшее из обеих.
Цель: убрать 3-5 дублей, не тратя на них токены Critic-а.

**2. Founder-fit check:**
Для каждой гипотезы ответить: "Захочет ли основатель работать с этой аудиторией
6-12 месяцев?" Если ответ "мне это чуждо" — KILL.
Если ответ "не знаю, но интересно" — оставить.

После dedup + founder-fit: 15-20 гипотез → Rule Compliance Check → API Pre-screen → Critic.

---

#### Rule Compliance Check (часть Round 1.5) — NEW в v8, обновлён в v10

Автоматическая проверка правил Generator перед отправкой в Critic.
Generator систематически нарушает правила (подтверждено в v7 run 1 + run 2:
ADHD CAP, blacklist #14, галлюцинация "Obsidian open-source").
Промпт не работает как ограничение — модель его игнорирует.

**Агент:** Haiku (дешёвый, ~8-15K токенов, 0-12 поисков)

```
Вот [N] JTBD-гипотез и правила генерации.

## Blacklist
[ВСТАВИТЬ BLACKLIST ИЗ METHODOLOGY]

## Whitelist (с лимитами)
[ВСТАВИТЬ WHITELIST ИЗ METHODOLOGY]

## Проверь каждую гипотезу:

### 1. Blacklist compliance
Для каждой гипотезы: попадает ли она под любой пункт blacklist?
- Если да → пометить BLACKLIST_VIOLATION с номером пункта

### 2. Фактические утверждения
Для каждой гипотезы: содержит ли она утверждения о лицензиях,
ценах, функциях конкурентов, статусе API?
- Если да → пометить FACT_CHECK_NEEDED с конкретной цитатой
  (например: "утверждает что Obsidian open-source — проверить")

### 3. Pattern Cap enforcement
- Посчитай гипотезы на каждый whitelist-паттерн. Лимит: max 4.
- Посчитай гипотезы на каждую персону. Лимит: max 2.
- Если превышено: ВЫБЕРИ лучшие (по confidence Generator-а),
  остальные → KILL с пометкой PATTERN_CAP_EXCEEDED.
  НЕ просто помечай — УБИВАЙ лишние. Это не рекомендация, а правило.

### 4. Free Alternative Pre-screen (NEW v9)
Для каждой выжившей гипотезы (после шагов 1-3) сделай 1 web search:
  "[product category] free alternative"
- Если находишь бесплатную альтернативу с 50K+ users,
  закрывающую тот же job → пометить FREE_ALT_KILL
- Если free альтернатива покрывает <50% job → PASS
- Цель: убить "race to the bottom" гипотезы ДО Critic

### 5. Competition Pre-screen (NEW v10)
Для каждой выжившей гипотезы (после шагов 1-4) сделай 1 web search:
  "[product name] app" или "[job description] app"
- Если находишь 3+ конкурента с 4+ рейтингом, закрывающих тот же job
  → пометить COMPETITION_KILL
- Если 1-2 конкурента с <4 рейтингом → PASS (gap вероятен)
- Если 0 конкурентов → PASS (blue ocean или нет рынка — Critic разберётся)
- Цель: поймать нишевых конкурентов (Screenotate, CLZ Books, Monarch Extension),
  которых Generator не знает из training data

> **v9-run7 lesson:** Generator не знал о Screenotate (exact same product как H10),
> CLZ Books ($20/год, offline + duplicate alert для H3), Pocket Casts (free clip
> sharing для H1). Critic потратил ~77K токенов, чтобы найти то, что 1 поиск
> нашёл бы в Rule Check за 0 токенов агента. Competition Pre-screen экономит
> ~40-60K токенов на заведомо мёртвых гипотезах.

### Выход
Таблица: | H# | Название | Blacklist? | Fact-check? | Pattern Cap? | Free Alt? | Competition? | Решение |
Решение: PASS / KILL (blacklist/cap/free alt/competition) / FLAG (fact-check нужен)

Гипотезы с KILL убираются. Гипотезы с FLAG передаются Critic-у
с пометкой "проверить утверждение X".
```

> **Зачем:** Generator в v7 трижды нарушил blacklist #14 (NFC-оборудование),
> трижды нарушил ADHD CAP, и дважды повторил галлюцинацию "Obsidian = MIT".
> Изменение промпта не помогло. Rule Check ловит нарушения до того,
> как Critic потратит поиски на невалидные гипотезы.
>
> **v9 lesson: Lead manual вместо Haiku.** Haiku тратит ~27K на reasoning
> и часто делает 0-1 tool_use. Lead вручную делает Rule Check за 5 мин
> с лучшим качеством. Рекомендация: Lead manual для всех проверок.
>
> **v9 change:** добавлены Pattern Cap enforcement (было только FLAG, теперь KILL)
> и Free Alternative Pre-screen (1 поиск на гипотезу). В v8 Pattern Cap
> был нарушён (7 pricing gap, 6 personal memory вместо max 4),
> а 7/12 гипотез убиты Critic из-за бесплатных альтернатив.
> Pre-screen Haiku (~12 поисков) экономит ~40-50K токенов Critic/Red Team/QV
> на заведомо мёртвых гипотезах.
>
> **v10 change:** добавлен Competition Pre-screen (шаг 5) — 1 поиск на гипотезу
> "[product name] app". Generator не имеет web search и не знает о нишевых
> конкурентах 2024-2026 (Screenotate, CLZ Books, Monarch Extension). Competition
> Pre-screen ловит их за 1 поиск до того, как Critic потратит ~10K на гипотезу.

---

#### API Pre-screen (часть Round 1.5) — NEW в v5

Для каждой гипотезы с полем `API Dependency: HIGH`:
- 1 web search: "[platform name] API public access developer"
- Если API закрыт / invitation-only / deprecated → **KILL** с пометкой "API BLOCKER"
- Если API публичный → оставить, пометить "API OK"

> **Зачем:** H4 в v4 (Airbnb Guest Deja Vu) прошёл через Critic (22 searches)
> и Validator (28 searches), чтобы в итоге умереть на "Airbnb API invitation-only".
> 1 поиск в Round 1.5 сэкономил бы ~30 searches и ~40K токенов.

Можно запустить как Haiku-агента или сделать вручную (1 поиск — 30 секунд).

---

### Раунд 2: Quick Kill (2-фазный Critic)
**Цель:** из 8-12 гипотез убить 60%+, оставить 3-5
**Время:** ~15-25 мин
**Токены:** ~40-70K (2 агента при <8 гипотез, 3 при 8+)
**Работает:** CRITIC (2 фазы или 2-3 параллельных мини-агента)
**Web search:** ДА, ОБЯЗАТЕЛЬНО — это ключевое отличие v4

> **v9 change:** Rule Check с Free Alternative Pre-screen убивает 4-6 гипотез
> до Critic. Critic получает ~8-12 вместо ~15-20. При <8 гипотезах запускать
> 2 мини-Critic-а (по 3-4 гипотезы), при 8+ — 3 агента. Экономия ~20K токенов.

> **Проблема v2-v3:** Critic получал 15 гипотез одним промптом и судил
> по training data, не делая ни одного web search. Вердикты были
> неточными — ложные KILL (убивал живое) и ложные ALIVE (пропускал мёртвое).

---

**Вариант A: 2-фазный Critic (последовательно)**

**Фаза A — Searcher (факты, не мнения):**

```
Вот [N] продуктовых JTBD-гипотез для B2C pet-project:
[ВСТАВИТЬ ГИПОТЕЗЫ]

## Твоя задача: ТОЛЬКО ИСКАТЬ, НЕ СУДИТЬ

Для КАЖДОЙ гипотезы сделай РОВНО 2 поисковых запроса:
1. "[ключевые слова продукта] app" — найти конкурентов
2. "reddit [целевая аудитория] [проблема]" — найти обсуждения

Для каждой гипотезы верни ТОЛЬКО ФАКТЫ:
- **Конкуренты:** название, цена, рейтинг, кол-во скачиваний (если нашёл)
- **Reddit/HN:** URL поста, количество upvotes, краткая цитата (если нашёл)
- **Если не нашёл ничего:** так и пиши "0 конкурентов найдено" / "0 постов найдено"

НЕ делай выводов. НЕ пиши KILL/ALIVE. Только факты.

ВАЖНО: ты ОБЯЗАН сделать web search для каждой гипотезы.
Если ты не сделаешь поиск — результат бесполезен.
НЕ используй site:reddit.com в запросах. Ищи "reddit [topic]" напрямую.
```

**Фаза B — Judge (вердикт по фактам):**

```
Вот [N] гипотез с результатами поиска по каждой:
[ВСТАВИТЬ РЕЗУЛЬТАТЫ ФАЗЫ A]

## Профиль основателя
[ВСТАВИТЬ]

## Твоя задача: вынести вердикт по каждой гипотезе

На основе ФАКТОВ (не своих знаний!) ответь на 4 вопроса:

### Quick Kill Questions:

1. **ALREADY SOLVED?**
   - Searcher нашёл 3+ конкурентов с 4+ рейтингом, закрывающих ЭТОТ ЖЕ JOB
     для ЭТОЙ ЖЕ аудитории → KILL (HIGH confidence)
   - Searcher нашёл конкурентов, но job overlap PARTIAL (смежный job, другой
     UX-подход, другая аудитория) → WEAK (LOW confidence, перепроверить)
   - Searcher нашёл 1-2 конкурента с 3-star → ALIVE (gap likely)
   - Searcher нашёл 0 конкурентов → ALIVE (blue ocean или нет спроса)
   - ОБА поиска вернули 0 релевантных результатов → KILL (нет рынка)

2. **FEATURE TRAP?**
   - Это уже фича в iOS/Android/Chrome? → KILL
   - Notion/Obsidian/Todoist могут добавить за спринт? → WEAK

3. **DISTRIBUTION REALITY?**
   - Searcher нашёл Reddit посты с 50+ upvotes? → +1
   - Можно описать в одном предложении для PH? → +1
   - Если 0 из 2 → KILL

4. **WHY DOESN'T THIS EXIST YET?**
   - Причина правдоподобна? Searcher не нашёл продукт, подтверждающий причину?
   - Если причина опровергнута фактами → KILL

### Вердикт: KILL / WEAK / ALIVE + Confidence: HIGH / LOW

- **HIGH confidence:** вердикт основан на фактах из Searcher
  (конкретные URLs, названия, цены)
- **LOW confidence:** факты неполные, Searcher не нашёл релевантных результатов.
  LOW confidence вердикты передаются Validator-у на перепроверку.

KPI: убить минимум 60%. Если убил меньше — ты слишком мягкий.
```

---

**Вариант B: 3 параллельных мини-Critic-а (быстрее)**

Вместо 2 фаз — запустить 3 агента параллельно, каждый проверяет 5 гипотез.
Промпт каждого включает И поиск, И вердикт:

```
Вот 5 продуктовых JTBD-гипотез:
[ВСТАВИТЬ 5 ГИПОТЕЗ]

Для КАЖДОЙ:
1. Сделай 2 web search запроса (обязательно!):
   a. "[ключевые слова продукта] app" — найти конкурентов
   b. "reddit [целевая аудитория] [проблема]" — найти обсуждения
   ВАЖНО: если продукт связан с Google Sheets, email, docs, calendar —
   ОБЯЗАТЕЛЬНО ищи в Google Workspace Marketplace:
   "[function] google workspace addon" или "[function] google sheets addon".
   Mailmeteor (7M), YAMM (10M) — примеры конкурентов, невидимых в Reddit/HN.
   Аналогично для Chrome extensions: "[function] chrome extension".
2. Ответь на 4 Quick Kill Questions (см. выше)
3. Вынеси вердикт: KILL / WEAK / ALIVE + Confidence: HIGH / LOW

ВАЖНО: без web search твой вердикт БЕСПОЛЕЗЕН. Ищи.
```

**Преимущества Варианта B:**
- 5 гипотез на агента = больше шансов что он реально поищет
- Параллельно = быстрее
- Проще промпт = меньше шанс что агент пропустит инструкции

**Harder Kill Rules (v7):**
- 3+ конкурентов с 4+ рейтингом, закрывающих ТОТ ЖЕ job = **auto-KILL** (было 5+ в v4)
- ОБА поиска вернули 0 релевантных результатов = **KILL** (рынка нет)
- Kill rate < 50% после раунда = Critic слишком мягкий, пересмотреть
- **FREE ALTERNATIVE — JOB OVERLAP CHECK (v7):** Searcher нашёл FREE tool с 100K+ users?
  Задай вопрос: "Закрывает ли этот бесплатный инструмент КОНКРЕТНЫЙ JOB гипотезы
  для КОНКРЕТНОЙ аудитории?"
  - **Job overlap HIGH** (тот же job, та же аудитория) → **KILL** (HIGH confidence)
    Пример: SyncOwn ($15) vs Remotely Save (FREE 100K+) — один и тот же job (sync Obsidian)
  - **Job overlap PARTIAL** (смежный job или другая аудитория) → **WEAK** (LOW confidence, перепроверить)
    Пример: HyperJar (FREE, ADHD budgeting) vs PileBudget (spatial piles) — оба для ADHD,
    но разный UX подход. Нужна перепроверка: достаточно ли отличается UX?
  - **Job overlap LOW** (другой job, общая категория) → **ALIVE**
    Пример: Medisafe (FREE, tap-to-log) vs Did I Dose? (NFC, без разблокировки) — разный job
  > **v6 lesson:** бинарный kill (FREE 100K+ = KILL) не различал прямых и непрямых
  > конкурентов. Job overlap оценивает конкретное пересечение, а не категорию.

---

### Раунд 2.25: Red Team (Devil's Advocate) — NEW в v7
**Цель:** найти причины провала КРОМЕ конкуренции
**Время:** ~10-15 мин
**Токены:** ~20-30K (1 Sonnet)
**Работает:** RED TEAM (1 агент)
**Web search:** ДА, 1-2 запроса на гипотезу
**Input:** ALIVE + WEAK гипотезы после Critic (5-8 штук)

> **Зачем:** Critic проверяет только конкуренцию (2 searches: competitors + Reddit).
> Но гипотезы умирают не только от конкурентов — есть regulatory risk (COPPA, HIPAA),
> unit economics (стоимость привлечения > LTV), retention patterns (one-time use),
> user behavior (problem не мотивирует к действию). Red Team ловит эти риски.
>
> **Не убивает.** Red Team добавляет risk flags, но не выносит вердикт KILL.
> Решение принимает Lead на основе flags + Critic verdict.

---

**Промпт для Red Team:**

```
Вот [N] выживших гипотез после Critic:
[ВСТАВИТЬ ALIVE + WEAK]

## Твоя задача: найти причины ПРОВАЛА, которые НЕ связаны с конкуренцией

Для КАЖДОЙ гипотезы ищи structural risks в 5 категориях:

### 1. REGULATORY RISK
- Нужна ли сертификация, лицензия, compliance (COPPA, HIPAA, GDPR, FDA)?
- 1 web search: "[product domain] regulatory requirements app"
- Если есть — severity: LOW (easy compliance) / MEDIUM (costly) / HIGH (blocker)

### 2. UNIT ECONOMICS RISK
- CAC для этой аудитории > $50? (medical, enterprise = дорого)
- LTV при указанной цене < $100/yr? (значит CAC должен быть < $10)
- Freemium conversion в этой категории < 2%?
- Reasoning only, без search.

### 3. RETENTION RISK
- Продукт решает проблему один раз? (one-time use = нет подписки)
- Аудитория перерастает проблему? (студенты заканчивают учёбу)
- Нет habit loop? (нет daily trigger для возврата)
- Reasoning only, без search.

### 4. BEHAVIOR RISK
- Альтернативное объяснение боли: поведение вызвано не тем, чем кажется?
  (пример v4: ADHD app hopping = dopamine seeking, не забывчивость)
- Люди ГОВОРЯТ что хотят это, но не ДЕЛАЮТ? (intention-action gap)
- Reasoning only, без search.

### 5. DISTRIBUTION RISK
- Primary channel имеет strict self-promotion rules? (r/ADHD, r/medicine)
- Viral mechanic отсутствует? (нет причины рассказать другу)
- ASO competition: если app — сколько apps по этому keyword?
- 1 web search: "[keyword] app store" (если mobile app)

### Выход: для каждой гипотезы
- Risk flags: 0-3 штуки, каждый с severity (LOW/MEDIUM/HIGH)
- Если 0 flags — пиши "No structural risks found"
- Если 2+ HIGH severity flags — пометить "RED FLAG"
- НЕ выноси вердикт KILL/ALIVE — только flags

ВАЖНО: ты devil's advocate, не cheerleader. Ищи причины ПРОТИВ.
Если не находишь серьёзных рисков — это хороший знак, не повод придумывать.
```

---

### Раунд 2.5: Quick Validator (Gate) — NEW в v5, обновлён в v8
**Цель:** дешёвая проверка перед дорогим Deep Validation
**Время:** ~5-10 мин (параллельно, Haiku)
**Токены:** ~10-20K (Haiku x N гипотез)
**Работает:** QUICK VALIDATOR (Haiku)
**Web search:** ДА, 4 запроса на гипотезу (было 3, добавлен App Store scan)
**Gate logic:** Запускается для ВСЕХ гипотез, даже для 1.

> **Зачем:** Deep Validator стоит ~20-30K токенов и ~30 минут на гипотезу.
> Quick Validator за ~3K и 2 минуты отсеивает blockers и гипотезы без T1 signal.
> 3 searches за ~3K дешевле 10+ за ~20K — всегда выгоден.
>
> **v5 lesson:** Quick Validator был ПРОПУЩЕН ("только 3 гипотезы, gate не нужен").
> Это anti-pattern — Quick Validator полезен ВСЕГДА (blocker check + T1 scan
> за 3 searches дешевле полного Deep Validation даже для 1 гипотезы).

---

**Промпт для Quick Validator-а:**

```
Вот [N] выживших гипотез после Critic:
[ВСТАВИТЬ ALIVE + WEAK с LOW confidence]

Для КАЖДОЙ гипотезы сделай РОВНО 4 web search запроса:

1. **Blocker check:** "[platform/API] developer access public API [year]"
   — Есть ли технический blocker? API закрыт? Platform TOS запрещает?

2. **T1/T1-alt scan:** Выбери запрос по типу категории:
   - Established category: "reddit wish there was [product description]"
   - Novel category (anti-pattern, personal memory): "reddit [workaround description] how to"
     или "reddit [job description] every day manually"
   — Для novel categories ищи workaround chains (T1-alt), не wish posts (T1).
     Люди не просят продукт, которого не могут представить — они описывают
     многошаговый обходной путь.

3. **Competition scan:** "[product type] app [year]"
   — Сколько конкурентов и какие цены?

4. **App Store scan:** "best [job description] app site:apps.apple.com OR site:play.google.com"
   — Есть ли нативные конкуренты в магазинах приложений?

> **v7-run2 lesson:** Quick Validator с 3 поисками пропустил MonAi (4.8 звезд,
> 8.5K отзывов, iOS native) для H24 VoiceExpense и Contacts Journal ($20,
> 4.7 звезд, 10+ лет) для H7 NetMeet. Оба были найдены только в Deep Validation.
> 4-й запрос по App Store ловит нативных конкурентов, невидимых в Reddit/HN.

### Вердикт для каждой:
- **PASS** → Deep Validator (нет blocker, есть хоть 1 signal)
- **BLOCK** → KILL (технический blocker найден, указать какой)
- **NO_SIGNAL** → KILL (0 signals после 4 запросов = demand unproven)

ВАЖНО: это gate, не deep analysis. 4 запроса, короткий вердикт. Без эссе.
```

---

#### Best Available Carry-Forward (NEW v11)

Если после Quick Validator 0 survivors — **лучшая WEAK-гипотеза автоматически идёт
в Deep Validator** с тегом `CONDITIONAL`.

**Правила выбора Best Available:**
1. Из всех гипотез, убитых на стадиях Critic → Red Team → Quick Validator,
   выбрать ту, которая прошла дальше всех по пайплайну
2. При равной глубине — выбрать с наименьшим количеством HIGH-severity risk flags
3. При равенстве — выбрать с лучшим demand signal tier (T1.5 > T2 > T3)

**Что происходит:**
- Deep Validator работает как обычно (blocker-first, 10-15 searches)
- Synthesis пишет полное досье с вердиктом `WEAK — [причины]`
- Досье включает секцию **"What Would Need to Be True"** — конкретные условия,
  при которых гипотеза стала бы MODERATE (какой demand evidence нужен,
  какой gap должен подтвердиться, какой риск должен не реализоваться)
- Файл создаётся в `finalists/` с тегом `conditional: true` в метаданных

**Зачем:**
- Пустой прогон = ~$1-2 без выхлопа. WEAK-досье с анализом "что должно быть правдой" —
  ценнее нуля
- Данные для cross-run сравнения: паттерн может проявиться через 5-10 прогонов
- Секция "What Would Need to Be True" — checklist для ручной валидации

> **v10 lesson:** 2 прогона v10 дали 0 финалистов. Лучшие гипотезы (H8 SeasonPass v10-run1,
> H6 Creator Finance Sync v10-run2) были убиты на Critic и Quick Validator соответственно.
> Их досье были бы ценнее пустого вывода — анализ "почему WEAK" содержит рыночный
> инсайт, который теряется при просто KILL.

---

### Раунд 3: Deep Validation
**Цель:** для 2-4 прошедших Quick Validator — глубокая проверка demand + distribution
**Время:** ~30-40 мин
**Токены:** ~50-80K (1-2 агента параллельно)
**Работают:** 1-2 DEEP VALIDATOR-а
**Web search:** ДА, глубокий (10-15 запросов на гипотезу)
**Input:** гипотезы с вердиктом PASS из Round 2.5 + CONDITIONAL (Best Available, v11)

> **v9 change: RED FLAG skip rule.** Если Red Team пометил гипотезу RED FLAG
> (2+ HIGH severity risks) И Quick Validator не нашёл сильного T1 signal —
> НЕ отправлять в Deep Validation. Записать в Synthesis как "BACKUP with caveats".
> В v8 ReadStash (RED FLAG + PASS) получил ~25K токенов Deep Validation,
> чтобы подтвердить то, что Red Team уже нашёл. Lead override: если RED FLAG
> гипотеза имеет T1 signal — отправить в Deep Validation с пометкой.

> **Blocker-first strategy (v5):** Validator СНАЧАЛА проверяет технические blockers
> (API access, platform TOS, data availability), и только ПОТОМ тратит searches
> на demand evidence. Если blocker найден — KILL сразу, не тратя оставшиеся searches.
> Это сэкономило бы ~20 searches на H4 в v4.

---

**Промпт для Validator-а:**

```
Вот [N] выживших JTBD-гипотез:
[ВСТАВИТЬ ALIVE + лучшие WEAK + LOW confidence KILLs]

Для КАЖДОЙ гипотезы проведи глубокую проверку.
ВАЖНО: используй BLOCKER-FIRST стратегию — порядок секций имеет значение.

## 0. Blocker Check (ПЕРВЫМ ДЕЛОМ!)

Если у гипотезы есть API Dependency = HIGH или любая platform-зависимость:
- 1-2 web search: "[platform] API access", "[platform] developer program"
- Если API закрыт / invitation-only / deprecated → **KILL НЕМЕДЛЕННО**
- НЕ трать searches на demand evidence для заблокированной гипотезы
- Если blocker НЕ найден → продолжай к секциям 1-4

## 1. Demand Evidence (есть ли спрос?)

Используй ШАБЛОНЫ ПОИСКОВЫХ ЗАПРОСОВ:

### Для T1 evidence (прямые запросы):
- "reddit looking for [product type]"
- "reddit is there an app that [job]"
- "reddit wish there was [solution]"
- "hacker news ask hn [problem]"
- "[competitor name] alternative reddit"

### Для T2 evidence (жалобы):
- "[competitor name] app store reviews"
- "[competitor name] reddit complaints"
- "[competitor] doesn't [missing feature]"
- "[competitor] 1 star review"

### Для T1.5/T3 evidence (поведенческие/косвенные):
- "reddit [описание ситуации из job statement]"
- "[целевая аудитория] [проблема] frustration"
- "[целевая аудитория] forum [ключевое слово проблемы]"

Для каждого evidence:
- URL
- Цитата
- Engagement (upvotes, comments)
- Дата (свежесть)
- **Tier:**
  - **T1 (прямой запрос):** Reddit/HN пост "I wish X existed",
    "looking for X", "is there an app that does X?" с 50+ upvotes.
    Это ЛУЧШИЙ тип evidence.
  - **T1-alt (workaround chain):** Человек описывает многошаговый
    обходной путь (3+ шагов), который выполняет регулярно, с evidence
    повторяемости (несколько постов, "every day I do X then Y then Z",
    или guide с 50+ upvotes). Человек платит ВРЕМЕНЕМ за решение job —
    это доказывает спрос действием. Эквивалент T1 для novel categories,
    где "wish X existed" не появляется (люди не знают, как назвать продукт).
    Правило: 1x T1-alt = 1x T1 по весу.
    > **v6 lesson:** ни одна гипотеза за v3-v6 не получила T1. Корневая
    > причина: метод JTBD-пересечений находит gaps слишком novel для
    > explicit demand. T1-alt ловит спрос, выраженный поведением, а не словами.
  - **T1.5 (поведенческий сигнал):** Reddit/HN пост описывающий
    СИТУАЦИЮ из job statement (не запрос на продукт) с 100+ upvotes.
    Или: конкурент с 10K+ downloads и рейтингом < 4.0 (люди платят,
    но недовольны). Правило: 2x T1.5 = 1x T1 по весу.
  - **T2 (жалоба на альтернативу):** 1-2 star review "this app
    doesn't do X" или "I switched because X was missing".
  - **T3 (косвенный):** статья, исследование, обзор рынка,
    упоминание проблемы без прямого запроса на решение.

### Scoring:
- Минимум 3 evidence на гипотезу
- STRONG demand: минимум 1x T1, или 2x T1.5, или 1x T1.5 + 2x T2
- MODERATE demand: минимум 1x T2 + 2x T3
- WEAK demand: все evidence T3
- KILL: < 3 evidence

## 2. Competition Landscape

- Топ-5 ближайших альтернатив
- Для каждой: название, downloads/MAU, рейтинг, цена
- GAP: что конкретно они делают плохо для ЭТОГО job?
- Если gap = "ничего, всё отлично" → KILL

## 3. Distribution Channels

- Primary channel: [конкретно — какой subreddit, какой keyword, какой сайт]
- Есть ли примеры похожих продуктов, которые выросли через этот канал?
- Product Hunt potential: запускались ли аналоги? Сколько upvotes?

## 4. Pricing & Path to $5K MRR

- Сколько платят за ближайшие аналоги?
- Pricing model: подписка / разовая / freemium
- Расчёт: $[цена] x [кол-во платящих] = $5K MRR
- Реалистичен ли этот путь за 6-12 месяцев?

## Итоговый вердикт: STRONG / MODERATE / WEAK / KILL

STRONG: demand evidence (T1, или T1-alt, или 2x T1.5) + clear gap + distribution + pricing
MODERATE: 3 из 4
WEAK: 2 из 4
KILL: < 2

ВАЖНО: НЕ используй site:reddit.com в поисковых запросах.
```

---

### Раунд 4: Final Synthesis
**Цель:** 2-3 финальных досье на выжившие гипотезы
**Время:** ~15-20 мин
**Токены:** ~30-40K (Lead может запустить агента для дополнительных поисков)
**Работает:** LEAD (может делегировать Sonnet-агенту для research)

Lead берёт STRONG/MODERATE гипотезы и для каждой составляет досье.
Если единственный финалист — CONDITIONAL (Best Available), вердикт = WEAK
с обязательной секцией "What Would Need to Be True".

```markdown
## [Название]

### Кто
[Конкретный человек — не "solopreneur", а "indie hacker, который в одиночку
ведёт SaaS с 50-500 пользователями, сам пишет код, сам отвечает на support".
2-3 предложения, чтобы читатель мог представить этого человека.]

### Ситуация
[Конкретный момент, когда боль возникает. Не абстрактно "нужно приоритизировать
фичи", а сценарий: что произошло, где человек, что он видит, что чувствует.
3-5 предложений.]

### Job to be Done
> Когда я [конкретная ситуация из блока выше],
> я хочу [конкретное действие — что именно сделать],
> чтобы [конкретный результат — что изменится].

### Как решают сейчас
[Что делают без нашего продукта. Какие инструменты/workarounds используют.
Почему это не работает. 2-3 предложения.]

### Продукт
[Конкретное описание что продукт ДЕЛАЕТ — не маркетинговое, а функциональное.
Перечислить 3-5 ключевых действий пользователя с продуктом.
Читатель должен понять механику, не открывая прототип.]

Цена: [$X/mo]

### Demand Evidence
- [3+ ссылок на реальные запросы/жалобы с цитатами]

### Конкуренция

| Альтернатива | Цена | Gap для нашего job |
|---|---|---|

### What Would Need to Be True (для CONDITIONAL/WEAK)
- **Demand:** [какой evidence нужен? T1 wish с 50+ upvotes? T1-alt workaround chain?]
- **Gap:** [какой gap должен подтвердиться? Конкурент X не добавит фичу Y?]
- **Risk:** [какой structural risk должен не реализоваться?]
- **Test:** [конкретный способ проверить за 1-2 дня без кода]

```

---

### Раунд 4.5: Досье финалистов

**Цель:** подробное описание каждого финалиста в отдельном файле с вики-ссылками
**Время:** ~5-10 мин
**Работает:** LEAD

После синтеза Lead создаёт файл в `finalists/` для каждой гипотезы с вердиктом MODERATE или STRONG.

**Формат файла:** `finalists/[Название].md`

**Язык:** чистый русский. Технические термины (JTBD, demand signal, kill rate, MVP, PMF, LTV, CAC) допускаются без перевода. Всё остальное — по-русски. Никакого Runglish ("gap confirmed", "job validated", "competition saturated"). Писать живым языком, как будто объясняешь другу, а не роботу.

**Обязательные секции:**
- Метаданные (YAML): hypothesis, run, verdict, date, demand, gap, distribution, pricing, risk, buildable, price, target_mrr, users_needed
- Для кого (конкретный человек, 2-3 предложения)
- Боль (сценарий из жизни, 3-5 предложений — читатель должен узнать себя)
- Задача (JTBD формулировка на русском: "Когда я..., я хочу..., чтобы...")
- Сценарии использования (2-3 конкретных примера: что делает пользователь, как продукт помогает)
- Как решают сейчас (текущие костыли и их недостатки)
- Продукт (3-5 функций, описание MVP)
- Доказательства спроса (таблица с уровнями T1-T3, цитаты переведены на русский)
- Конкуренция (таблица: альтернатива, цена, чего не хватает)
- Структурные риски (оценка Red Team)
- Сильные и слабые стороны (кратко, по 2-3 пункта)
- Путь к $5K/мес (таблица: цена, нужно клиентов, конверсия, каналы)
- Рекомендация (конкретный следующий шаг для валидации)

**Вики-ссылки:**
- Между финалистами одного прогона: `[[StudioQueue]]`, `[[ReadStash]]`
- Индекс всех финалистов: `finalists/README.md`
- Обновлять индекс после каждого прогона

> **Зачем:** results.md содержит краткие описания всех прогонов, но для принятия
> решения "что строить" нужны самодостаточные досье с полным контекстом.
> Отдельные файлы позволяют сравнивать финалистов через Obsidian-граф
> и видеть связи между похожими идеями из разных прогонов.

---

## Cross-Run Learning

> После каждого прогона — обновлять эти списки.
> Generator и Critic получают их как контекст.

### Blacklist (паттерны убитых гипотез)

> **Формат v5:** каждый паттерн включает причину + конкретных конкурентов,
> чтобы Critic мог быстро верифицировать, а Generator — не повторять.

Не генерировать/не пропускать гипотезы с этими паттернами:

1. **Sleep/wellness apps для нишевых аудиторий** — subscription fatigue. *Конкуренты:* Timeshifter, Sleep Cycle, Calm, Headspace. *Убито в:* v1. Исключение: если gap = принципиально новый UX (например NFC)
2. **Micro-features (одна кнопка)** — "reprint last label", "show battery %" — это feature, не product. Не стоит как standalone. *Убито в:* v1-v2
3. **CLI tools для developers** — free expectations, невозможно монетизировать. *Убито в:* v2. Исключение: cloud sync с team features
4. **Scanner/analyzer apps для commodity data** — нельзя конкурировать с бесплатными incumbents. *Конкуренты:* Yuka (80M+), Fig, ingredient scanners. *Убито в:* v1. Исключение: personal memory angle
5. **Timezone/calendar converters** — слишком нишевые, free alternatives exist. *Убито в:* v2
6. **"AI wrapper for X" без конкретного job** — бесполезно как positioning. *Убито в:* v2-v3
7. **Airbnb cleaning/verification tools** — рынок насыщен. *Конкуренты:* Turno ($8/mo, 4.5+), Cleanster (GPS+photo), Turnify, Properly, ResortCleaning. *Убито в:* v4 (H18)
8. **YouTube thumbnail A/B testing** — рынок переполнен + YouTube native. *Конкуренты:* ThumbnailTest ($29-49/mo), TubeBuddy ($30-50/mo), YouTube Test & Compare (FREE, 50K+ creators), ViewStats, VidIQ. *Убито в:* v4 (H5)
9. **Substack comment management** — Substack native moderation покрывает 80%. *Убито в:* v4 (H3)
10. **Notion template version control** — Synced blocks + email уже решают. *Убито в:* v4 (H7)
11. **ADHD receipt/expense voice logging** — Apple Notes (photo+voice, FREE) + Expensify ($5/mo). *Убито в:* v4 (H2)
12. **ADHD app graveyard tracker** — misdiagnosis: поведение вызвано dopamine-seeking, не забывчивостью. Tracker не решает root cause. *Убито в:* v4 (H13)
13. **Platform-dependent products без публичного API** — если MVP зависит от invitation-only API, это blocker. *Пример:* Airbnb API — invitation-only. *Убито в:* v4 (H4)
14. **Products requiring additional hardware** — NFC-теги, физические устройства, датчики, кастомные аксессуары. Доп. оборудование = logistics, fulfillment, support complexity, несовместимые с solo-developer constraint. *Примеры:* NFC app blockers (Brick, Unpluq), NFC pill trackers, custom hardware. *Убито в:* v7 (H6 FocusLock, v2 Did I Dose). Исключение: если hardware = commodity (стандартный NFC-стикер $0.50) И продукт полностью software — тогда допустимо, но помечать HARDWARE_RISK
15. **ADHD/neurodivergent productivity apps** — ПОЛНЫЙ ЗАПРЕТ. Рынок на $4B, проблема реальна, но нет работающей методологии. Executive dysfunction = целевая аудитория не может регулярно использовать приложения. Все существующие игроки борются с retention: Habitica (наказывает → стыд → бросают), Forest (таймер, не решает initiation), Tiimo (App of Year, но retention неизвестен), Finch (питомец "умирает" → бросают). 5 из 7 прогонов генерировали ADHD-финалистов (FlowGuard, FocusLock, DailyPuzzle, QuestTask, HyperfocusGuard) — ни один не имеет пути к устойчивому бизнесу. *Убито в:* v2-v7 (системный вывод). БЕЗ ИСКЛЮЧЕНИЙ

### Whitelist (паттерны выживших гипотез)

Приоритизировать гипотезы с этими паттернами:

1. **Pricing gap $50→$15** — incumbent дорогой, solopreneurs ищут дешевле (Feature Memory vs Canny)
2. **Personal memory (вместо shared database)** — "ты это уже покупал/делал" — gap, который incumbents не закрывают (они фокусируются на analysis, не на memory)
3. ~~Physical verification (NFC/hardware)~~ — **УБРАН в v7:** hardware = logistics burden для solo dev. Перенесён в blacklist #14
4. **"Anti-pattern as feature"** — то, что mainstream считает bad UX (fullscreen alerts, DND override), но нишевая аудитория ХОЧЕТ
5. **Solopreneur/indie hacker audience** — founder IS the audience, идеальный founder-market fit

> **v7 change:** "ADHD audience" убран из whitelist. Не помогло — 5 из 7 прогонов
> генерировали ADHD-финалистов. ADHD CAP (max 1) тоже не помог — Generator
> игнорирует ограничение.
>
> **v8 change:** ADHD/ND в полном blacklist (#15). Категория без работающей
> методологии: executive dysfunction = целевая аудитория не может регулярно
> использовать приложения. Все существующие игроки борются с retention.

---

## Параметры

| Параметр | Значение | Когда менять |
|---|---|---|
| Гипотез на входе | 20 | v8 было 25 — 13/25 убиты до Critic. 20 = оптимум |
| Scout-B сигналов | 10-15 | Было 15-20, но 40% = шум (PRICING_GAP). Качество > количество |
| Quick Kill threshold | 60% | Повысить если Critic слишком мягкий |
| Rule Check: Free Alt | Lead manual, 1 поиск | Убивает "race to bottom" ДО Critic. Lead > Haiku |
| Rule Check: Competition | Lead manual, 1 поиск (Sonnet) | Ловит нишевых конкурентов, невидимых Generator. Sonnet >> Haiku (v10 lesson) |
| Scout freshness check | 1 поиск на старый сигнал | Отсеивает сигналы, где боль уже закрыта рынком |
| Scout Signal Quality Gate | Lead manual, >= 3 T1/T1-alt | Предотвращает прогон на заведомо слабом input (v11) |
| Spot-check validation | Lead, 2 поиска | Проверяет конвертируемость T1/T1-alt potential (v12) |
| Scout-C depth pass | Sonnet, 9-15 поисков | Углубление 3-5 лучших сигналов (v12) |
| Generator Evidence Anchor | Правило 12, GROUNDED/SPECULATIVE | Маркировка source of features (v12) |
| Best Available carry-forward | Lead manual | Гарантирует непустой выхлоп каждого прогона (v11) |
| Quick Validator gate | Обязательный | Haiku, 4 searches — дешёвый фильтр |
| Saturated market ban | 5+ established players, 14 категорий | Generator не генерирует в зрелых рынках |
| RED FLAG → skip Deep Val | Да (если нет T1) | Lead override если T1 signal найден |
| Survivors для deep validation | 2-4 | Больше — дорого по токенам |
| Финальные идеи | 2-3 | Не больше 3 |
| Feature trap test | Обязательный | Главный killer для B2C |
| Distribution test | Обязательный | Нет канала = нет продукта |

### Бюджет одного прогона

| Раунд | Кто | v8 actual | v10-r1 | v10-r2 | v11 budget |
|--------|--------|----------|----------|----------|----------|
| Round 0: Scout | 2 Scout-а (Sonnet) | ~80K (~30 srch) | ~60K (~25 srch) | ~70K (~30 srch) | ~80-110K (~40-60 srch, +freshness) |
| Round 0.5: Signal Quality Gate | Lead manual | — | — | — | ~0K (Lead manual) |
| Round 0.75: Spot-check + Scout-C | Lead + Sonnet | — | — | — | ~17-22K (~2 spot-check + ~15 Scout-C depth) |
| Round 1: Generate | 1 Generator (Sonnet) | ~40K (0 srch) | ~32K (0 srch) | ~32K (0 srch) | ~30-35K (0 srch) |
| Round 1.5: Rule Check + Dedup | Lead manual (Sonnet srch) | ~5K (0 srch) | ~0K (~13 srch) | ~0K (~20 srch) | ~0K (Lead manual, +competition srch) |
| Round 2: Quick Kill | 2-3 Critic-а (Sonnet) | ~70K (~24 srch) | ~30K (~4 srch) | ~76K (~14 srch) | ~40-60K (~14 srch) |
| Round 2.25: Red Team | 1 Sonnet | ~20K (~8 srch) | — (0 survivors) | ~36K (~4 srch) | ~25-35K (~8 srch) |
| Round 2.5: Quick Valid. | Haiku | ~15K (~20 srch) | — (0 survivors) | ~33K (~4 srch) | ~15-25K (~8 srch) |
| Round 2.75: Best Available | Lead manual | — | — | — | ~0K (если 0 survivors) |
| Round 3: Deep Validate | 1-2 Validator-а (Sonnet) | ~55K (~33 srch) | — (0 survivors) | — (0 survivors) | ~35-50K (~20 srch, включая CONDITIONAL) |
| Round 4: Synthesis | Lead | ~15K (0 srch) | ~5K (manual) | ~5K (manual) | ~5-15K (WWNBT для CONDITIONAL) |
| **Итого** | | **~300K** | **~155K** | **~290K** | **~270-370K** |

> **v10 actuals:** 2 прогона, ~445K суммарно, 0 финалистов. v10-run1 (~155K) остановился
> на Critic (90% kill rate на Haiku Competition Pre-screen). v10-run2 (~290K) дошёл
> до Quick Validator, но demand T2.5 — недостаточно для MODERATE.
>
> **Эффективность по прогонам:**
> - v2: 230K → 3 финалиста (77K/финалист) — baseline
> - v5: 349K → 1 финалист (349K/финалист)
> - v6: 310K → 3 финалиста (103K/финалист) — best post-v2
> - v8: ~300K → 2 финалиста (~150K/финалист)
> - v9 (7 runs): ~2.3M → 1 финалист (~2.3M/финалист) — worst efficiency
> - v10 (2 runs): ~445K → 0 финалистов — input quality проблема подтверждена
> - v11 (1 run): ~300K → 1 WEAK (CONDITIONAL) — Best Available activated, core differentiator unvalidated
> - v12 (2 runs): ~862K → 2 CONDITIONAL (~431K/финалист) — Best Available стабилен, но quality = WEAK
> - v13 (1 run): ~461K → 1 CONDITIONAL — Goal Graph снизил competition, но не повысил demand

---

## Антипаттерны

1. **Категорийное мышление** — "ещё один [категория]-app". Если идея описывается категорией — это не пересечение. Пересечение = [Кто] + [Ситуация] + [Ограничение]

2. **"AI-powered X"** — AI как маркетинг, а не как решение job. Если убрать AI и job не решается — ОК. Если убрать AI и ничего не меняется — плохо

3. **"Я построю и они придут"** — distribution ДО product. Конкретный канал, конкретный subreddit, конкретный keyword

4. **"Feature, not a product"** — если это фича существующего инструмента, а не отдельный job — не продукт

5. **"Scope creep на этапе идеи"** — MVP = 1-2 экрана. Если больше — режь

6. **"Platform-first thinking"** — "хочу iOS app" вместо "хочу решить job X". Платформа — следствие job, не причина

7. **"Research rabbit hole"** — бесконечный анализ вместо генерации. В v2 research только для выживших, не для генерации

8. **"Critic без фактов"** — если Critic не сделал web search, его вердикты основаны на training data и могут быть галлюцинациями. Любой Critic output с 0 tool_uses = ненадёжен, нужно перезапустить или передать всё в Validation

9. **"Diversity ради diversity"** — 25 гипотез из 25 разных доменов = каждая поверхностная. Лучше 25 гипотез из 12-15 доменов с 2-3 вариантами для лучших

10. **"Generator без внешних данных"** — v3-v4 показали: Generator на чистом training data производит правдоподобные, но незаземлённые гипотезы. 0 STRONG за 2 прогона. Demand signals от Scout-ов — необходимый input

11. **"Validator тратит searches до проверки блокеров"** — v4 H4: ~28 searches на demand evidence, а потом "API invitation-only" = KILL. Blocker-first strategy: сначала 1-2 searches на blocker, потом остальные на demand

12. **"Pattern clustering"** — Generator без cap производит 9/25 гипотез с одним паттерном ("personal memory" в v4). Pattern cap (max 4 на паттерн) + demand signals от Scout-ов предотвращают это

13. **"Pricing gap = opportunity" fallacy** — pricing gap НЕ равен gap в job execution. Если FREE альтернатива закрывает job (Remotely Save 100K+, tawk.to unlimited), pricing gap бессмысленен. Pricing gap валиден ТОЛЬКО если free tool НЕ решает job (setup слишком сложен / platform mismatch / UX barrier для конкретной аудитории)

14. **"Scout quantity > Scout quality"** — 40 demand signals выглядят как богатый input, но если 70% — pricing complaints в red ocean, это хуже 10 signals в emerging behaviors. Scout должен приоритизировать workarounds и emerging, НЕ complaints в существующих категориях

15. **"Quick Validator gate на количество"** — логика "если < 5 гипотез, пропустить Quick Validator" делает gate бесполезным при агрессивном Critic. Quick Validator полезен ВСЕГДА: blocker check + T1 scan за 3 searches (Haiku ~3K) дешевле 10+ searches (Sonnet ~20K) в Deep Validator

16. **"Loudest community = best market"** — r/ADHD (1.5M+) генерирует больше upvotes и workaround-постов чем любая другая ниша → Scout находит ADHD-сигналы → Generator создаёт ADHD-пересечения → Validator подтверждает demand. 5/7 прогонов финалист = ADHD. Это structural bias + категория без работающей методологии. Решение v8: полный blacklist (#15), без исключений

17. **"Hardware = moat" fallacy** — NFC/физические устройства кажутся defensible moat, но для solo dev = logistics nightmare (fulfillment, shipping, returns, compatibility). Плюс Foqos (FREE, open-source, NFC) доказал что software-only конкуренты МОГУТ клонировать NFC-подход

18. **"ADHD app = viable product" fallacy** — рынок ADHD-приложений ($4B) выглядит привлекательно, но у категории нет работающей методологии решения проблемы. Целевая аудитория по определению не может регулярно использовать приложения (executive dysfunction → забрасывают через 2-3 недели). Habitica, Forest, Tiimo, Finch — все борются с retention. Проблема реальна, но программный продукт её не решает. 5 из 7 прогонов генерировали ADHD-финалистов — ни один не дошёл до валидации как жизнеспособный бизнес

19. **"Mature market + pricing gap = opportunity" fallacy** — Generator видит demand signal "X too expensive" и генерирует "cheaper X". Но в зрелых рынках (grammar, time tracking, meeting memory, sheets automation, personal CRM) уже есть 5-10+ players, включая бесплатные. Pricing gap =/= market gap. Три пустых прогона подряд (v7-r2, v9-r1, v9-r2) — все с Generator drift в mature markets. Исправлено: правило #11 (saturated market ban)

20. **"Google Workspace invisible competitors"** — add-ons в Google Workspace Marketplace (Mailmeteor 7M, YAMM 10M) не видны в Reddit/HN/Product Hunt. Critic с 2 web searches не найдёт их. Generator тоже не знает. Только Deep Validator (10+ searches) раскапывает. Решение: Critic обязан искать в Workspace Marketplace для Google-related гипотез

21. **"Stale signal = valid demand" fallacy** — Scout находит жалобу 2022 года и считает её demand signal. Но рынок реагирует быстрее пайплайна: Pocket Casts добавил клипы, Monarch Extension закрыл Amazon-боль, 5+ альтернатив заменили Chartable. Сигнал старше 6 месяцев без freshness check — liability, не asset. Решение v10: Scout Freshness Check (1 доп. поиск на старый сигнал)

22. **"Generator blind to niche competitors"** — Generator рассуждает по training data и не знает о нишевых продуктах 2024-2026: Screenotate (точная копия H10 ScreenDig), CLZ Books ($20/год для H3 BookShelf Scout), Monarch Extension (ML categorization для H2 ReceiptLine). Critic тратит ~10K токенов на каждую, чтобы найти очевидного конкурента. Решение v10: Competition Pre-screen в Rule Check (1 поиск на гипотезу)

23. **"Empty output = normal" fallacy** — "пустой прогон — нормально" (lesson 35) было верно для единичного случая, но 4 пустых прогона из 5 (v7-run2, v9-run1, v9-run2, v10-run1, v10-run2) — системная проблема. Прогон за ~$1-2 без выхлопа — потеря денег и знаний. Каждый прогон должен производить минимум 1 досье, пусть WEAK. Решение v11: Best Available carry-forward

24. **"T1 search for novel categories"** — Quick Validator ищет "wish there was [product]" для всех гипотез, включая novel categories (anti-pattern, personal memory). Но в novel categories люди не знают, как назвать продукт — они описывают workaround chain. Поиск T1 для novel category = гарантированный NO_SIGNAL → KILL. Решение v11: T1-alt search (workaround chains) для novel categories

25. **"Generator invents features from reasoning"** — Scout находит job ("developer clipboard underserved"), Generator добавляет feature из reasoning ("auto-tag by IDE project"). Feature не из evidence = hallucination, которую Validator не может подтвердить. 23 поиска — 0 results. Решение v12: Evidence Anchor (правило 12), маркирует GROUNDED vs SPECULATIVE

26. **"Signal potential ≠ signal convertibility"** — Quality Gate проверяет "есть ли T1/T1-alt potential?" (абстрактная оценка). Но потенциал ≠ конвертируемость: сигнал может выглядеть как T1-alt potential, но при поиске 0 results. Решение v12: Spot-check (2 поиска за ~2K перед Generator)

27. **"Scout breadth-first = Generator abstraction"** — 10-15 поисков → 15-20 сигналов = ~1 поиск на сигнал. Каждый сигнал — одна фраза без контекста. Generator получает абстракцию вместо конкретики и заполняет gaps из reasoning (hallucination). Решение v12: Scout-C depth pass (3 поиска x 3-5 сигналов)

28. **"Productivity porn" = жалобы без WTP** — indie devs/founders ГОВОРЯТ что ненавидят changelogs (H6), decision journals (H14), context briefings (H1). Но на практике не используют инструменты для их решения. Бесплатная альтернатива = "просто не делать" (не писать changelogs, не вести journal). Жалоба ≠ demand. Тест: если "ничего не делать" = viable workaround, product не нужен. v13-run1: 3 из 7 survivors имели этот паттерн

29. **"Goal Graph PREVIOUS = low competition + low demand"** — атака на предыдущие шаги goal hierarchy (PREVIOUS) снижает конкуренцию (47% Competition kill vs 62.5%), но одновременно снижает demand (71% QV NO_SIGNAL). Гипотезы слишком далеки от осознанной боли — люди не ищут решения для проблем, которые не формулируют. Оптимум = SUBGOAL_KILL (единственный ALIVE H6 = SUBGOAL_KILL)

---

## Lessons Learned

### Из v1 (search-first)

1. **Search-first находит зрелые рынки.** Если искать "todo app complaints" — найдёшь todo-рынок с 50+ конкурентами. Генерация на пересечениях обходит эту проблему.

2. **Critic убивает всё в насыщенных категориях.** В v1 все 8 гипотез попали в категории с сильными лидерами (Cal AI $4M/mo, Routinery 5M users). Пересечения создают ниши, где лидеров нет.

3. **"Scratch your own itch" не работает для нишевого пользователя.** Если профиль использования необычный — личные боли не масштабируются.

4. **Research — bottleneck.** В v1 Round 1 (2 Scout-а) занял ~60 мин. В v2 Round 1 (генерация без поиска) — ~15 мин. Экономия на самом дорогом этапе.

### Из v2 (generate-first)

5. **Generator кластеризует по персонам.** Без явного правила diversity получается 3 гипотезы для content creators, 2 для medical residents. Исправлено: max 2 на персону, min 10 персон.

6. **Дубли тратят токены Critic-а и Validator-а.** H10 и H24 — по сути один job для solopreneurs. Lead должен мержить до отправки агентам. Добавлен Round 1.5.

7. **Косвенный evidence != прямой demand.** Научная статья "сон влияет на бег" не равна Reddit-посту "wish there was an app correlating my sleep and runs". Добавлены evidence tiers (T1/T2/T3).

8. **Founder-fit проверять ДО Critic-а.** Нет смысла тратить токены на валидацию гипотезы, если основатель не захочет работать с этой аудиторией. Добавлен founder-fit check в Round 1.5.

9. **"Почему не существует?" — ключевой вопрос.** Если job реален и продукта нет, есть структурная причина. Generator должен её назвать, Critic — проверить.

### Из v3 (strict generate)

10. **Critic не делает web search — системная проблема.** В обоих запусках (v2, v3) Critic завершал работу с 0 tool_uses. Промпт "сделай 1-2 поиска" недостаточен — модель оптимизирует скорость и пропускает поиск. Решение: 2-фазный Critic (Search → Judge) или 3 параллельных мини-агента с меньшим batch size (5 гипотез = больше шанс поиска).

11. **Diversity enforcement размывает глубину.** 15 персон из 10+ доменов = хорошее покрытие, но каждая идея "поверхностнее". Решение: tiered generation — сначала 30 широких, потом углубление top-10 (2-3 варианта продукта для каждого job).

12. **T1 evidence — слишком высокая планка для нишевых продуктов.** "I wish X existed" с 50+ upvotes — редкость. Люди описывают СИТУАЦИЮ ("I can't sleep after night shift"), а не ЗАПРОС НА ПРОДУКТ. Решение: добавить T1.5 (поведенческий сигнал) — описание ситуации с 100+ upvotes = evidence что боль массовая.

13. **Cross-run learning ускоряет Generator.** Blacklist убитых паттернов ("sleep apps = subscription fatigue") и whitelist выживших ("pricing gap = сильный signal") помогают Generator не повторять ошибки.

14. **v3 строже, но честнее.** 0 STRONG (vs 2 STRONG в v2) — не провал, а результат более честной оценки. "MODERATE в v3 ≈ STRONG в v2" по уровню доказательности.

### Из v4 (2-phase Critic)

15. **3 мини-Critic-а работают — это подтверждено.** 22 web search vs 0 в v2/v3. Маленький batch (5 гипотез) = модель реально ищет, а не пропускает инструкции. Это основной метод для v5+.

16. **Generator без demand signals кластеризует.** 9 из 25 гипотез v4 были вариациями "personal memory" — правдоподобно, но незаземлённо. Demand signals от Scout-ов предотвращают кластеризацию, давая разнообразные seed-ы.

17. **API blockers нужно проверять ДО Deep Validation.** H4 (Airbnb) прошёл Critic и Validator, потратив ~50 searches, чтобы умереть на "API invitation-only". 1 поиск в Round 1.5 сэкономил бы всё. Добавлены: поле API Dependency, API Pre-screen, blocker-first strategy.

18. **Misdiagnosis — реальная угроза.** H13 (ADHD Tool Graveyard) — боль реальна (люди скачивают 47 apps), но причина не та (dopamine-seeking, не забывчивость). Tracker не решает root cause. Добавлено поле "Alternative Explanation" в Generator.

19. **Confidence levels в Critic — полезная innovation.** HIGH (факты из URL) vs LOW (training data). LOW confidence KILL-ы идут на перепроверку к Validator, а не умирают молча. H8 (Churn Detective) был WEAK+LOW у Critic, но MODERATE у Validator.

20. **WORKAROUND — сильнейший demand signal.** Groove ($500K MRR) построил ручную email-систему для churn analysis. Это T1.5: не "wish X existed", а "built X myself" — доказывает demand действием, не словами.

### Из v5 (Demand Scout)

21. **Scout-B pricing gap trap.** Шаблоны "too expensive alternative" и "pricing complaints" нашли 14/20 PRICING_GAP signals → Generator создал гипотезы в red ocean → Critic убил 71%, находя бесплатные альтернативы (tawk.to, Remotely Save, Franz, Uptime Kuma). Scout-B должен искать workarounds и emerging behaviors, НЕ pricing gaps. Исправлено: приоритет WORKAROUND > EMERGING > PRICING_GAP.

22. **Generator FREE blind spot.** Training data не видит новые бесплатные продукты. Generator предложил SyncOwn ($15) — не зная про Remotely Save (FREE, 100K+ downloads). SupportBox ($15) — не зная про tawk.to (FREE, unlimited). Исправлено: обязательное поле FREE ALTERNATIVE CHECK с обоснованием.

23. **Quick Validator gate на количество — anti-pattern.** Логика "если < 5 гипотез, пропустить Quick Validator" сделала gate бесполезным при агрессивном Critic (71% kill → 3 гипотезы). Quick Validator полезен ВСЕГДА: 3 searches за ~3K дешевле 10+ за ~20K в Deep Validator. Исправлено: убран порог, запускается для всех.

24. **Demand signals =/= viable niches.** Реальные боли (Reddit complaints, pricing gaps) могут быть в перенасыщенных рынках. v2 (2 STRONG) искал шире — workarounds, emerging, новые платформы. v3-v5 (0 STRONG) искали в existing pain points. Scout должен искать "где рынка ещё НЕТ", не "где рынок дорогой".

25. **Critic 71% kill rate — правильная калибровка.** v5 Critic убил 71% vs target 60%+ — это НЕ over-aggressive. Он правильно убил red ocean идеи (pricing gaps с free alternatives). Проблема в Scout-B input, не в Critic. Harder kill rules (3+ конкурентов = auto-KILL) подтверждены.

26. **Synthesis = не manual.** v5 показал: Round 4 стоит ~34K токенов и 8 web searches (build plan specifics, ASO keywords, distribution data). Обновлён бюджет: manual → ~30-40K.

### Из v6 (workaround-first Scout)

27. **T1 порог не работает для novel categories.** За v3-v6 ни одна гипотеза не получила T1. Метод JTBD-пересечений находит gaps слишком novel — люди не знают, что хотят просить. Исправлено в v7: T1-alt (workaround chain 3+ шагов = эквивалент T1).

28. **Whitelist "ADHD audience" создаёт bias.** 5 из 10 финалистов v2-v6 были в ADHD-нише. Это bias от whitelist, не от спроса. ADHD community имеет tool fatigue. Исправлено в v7: убран из whitelist, появляется органически через Scout.

29. **Бинарный FREE auto-kill ложно убивает.** "FREE 100K+ = KILL" не различает прямых и непрямых конкурентов. Medisafe (FREE, tap-to-log) и Did I Dose? (NFC) имеют разный job, но бинарное правило убило бы обоих. Исправлено в v7: job overlap check (HIGH/PARTIAL/LOW).

30. **Critic проверяет только конкуренцию.** Гипотезы умирают от regulatory risk (COPPA), unit economics (CAC > LTV), retention (one-time use), behavior (intention-action gap). Critic этого не ловит. Исправлено в v7: Red Team agent ищет structural risks в 5 категориях.

31. **v2 STRONG = v6 MODERATE.** v2 Critic не делал web search (0 tool_uses) → завышенные вердикты. Feature Memory и Did I Dose? получили бы MODERATE по стандартам v6. "Деградация" v3-v6 — не ухудшение генерации, а повышение честности оценки.

### Из v7-run2 (повторный прогон)

32. **Quick Validator слеп к App Store.** 3 веб-запроса уходят в Reddit/HN — нативные конкуренты в App Store проскакивают. MonAi (4.8 звезд, 8.5K отзывов) для H24 и Contacts Journal ($20 разово, 4.7 звезд) для H7 найдены только в Deep Validation. Исправлено в v8: 4-й обязательный запрос по App Store.

33. **Промпт Generator не работает как ограничение.** Те же нарушения в run 1 и run 2: ADHD CAP (3 вместо 1), blacklist #14 (3 NFC), галлюцинация "Obsidian open-source (MIT)". Изменение формулировки промпта не помогает — модель оптимизирует генерацию, а не compliance. Исправлено в v8: Rule Compliance Check (Haiku-агент проверяет правила после генерации).

34. **ADHD — категория без методологии.** 5 из 7 прогонов генерировали ADHD-финалистов: FlowGuard, FocusLock, DailyPuzzle, QuestTask, HyperfocusGuard. Ни один не жизнеспособен. Проблема реальна ($4B рынок), но executive dysfunction = целевая аудитория не может регулярно использовать приложения. Нет работающего решения. Исправлено в v8: ADHD в полном blacklist (#15), без исключений.

35. **Пустой прогон — нормально.** v7-run2 дал 0 выживших. Для поискового процесса ожидаемая вероятность пустого прогона ~20-30%. Не повод менять пайплайн — повод проверить, не исчерпано ли пространство поиска.

### Из v9-run1 и v9-run2

36. **Lead manual Rule Check > Haiku.** Haiku Rule Check (v9-run1) потратил ~27K токенов на reasoning и сделал 1 tool_use — Free Alt Pre-screen де-факто не выполнен. Lead manual (v9-run2): 5 минут, 0 токенов, поймал ChatGPT Memory FREE и Ollama+Open WebUI. Качество выше, стоимость ниже. Рекомендация: Rule Check всегда Lead manual.

37. **Google Workspace Marketplace — слепая зона.** Ни Generator, ни Critic не знали о Mailmeteor (7M установок, $12.99/мес) и YAMM (10M установок, $50/год) — Google Sheets add-ons, невидимые в Reddit/HN. Deep Validator нашёл, но потратил ~54K токенов. Исправлено: Critic обязан искать в Workspace Marketplace для Google-related гипотез.

38. **Privacy paradox — intention-action gap.** H4 PrivacyPulse (E2EE period tracker) убит Red Team: Flo 380M+ скачиваний несмотря на скандал с Facebook. Drip и Euki (бесплатные E2EE) существуют с 2019 и не набрали аудиторию. Пользователи ГОВОРЯТ про приватность, но ВЫБИРАЮТ удобство. Privacy-first как UVP не конвертируется в переключение для mass market health apps.

39. **Knowledge base trap.** H20 CodePatterns (snippet library) убит Red Team: "create once, never read". Разработчики предпочитают спросить коллегу, а не искать в документации — social behavior, не tooling problem. GitHub Wiki, Notion knowledge bases, internal docs — все страдают от того же паттерна. Гипотезы с knowledge management для команд — высокий retention risk.

40. **Три пустых прогона подряд — системный сигнал.** v7-run2, v9-run1, v9-run2 — 0 финалистов. Critic kill rate 100% (KILL+WEAK) в обоих v9 прогонах. Проблема не в фильтрах (они находят реальных конкурентов), а в **input quality**: Generator дрейфует в зрелые рынки. Исправлено: правило #11 (saturated market ban) запрещает категории с 5+ established players.

### Из v9-run7 (100% kill rate)

41. **Scout сигналы устаревают.** Scout находит реальные боли, но рынок их уже закрыл. B8 (podcast clips) → Pocket Casts добавил clip sharing в 2024. B3 (Amazon line items) → Monarch Extension запустился в 2024. A17 (Chartable shutdown) → 5+ альтернатив за год. Scout не проверяет, была ли боль уже закрыта. Исправлено в v10: Freshness Check — 1 доп. поиск на сигнал старше 6 месяцев.

42. **Generator слеп к нишевым конкурентам.** Правило #11 ловит очевидные категории (habit trackers, CRM), но не ловит нишевые продукты (Screenotate, CLZ Books, Monarch Extension). Generator не имеет web search — не может проверить, решена ли проблема. Исправлено в v10: Competition Pre-screen в Rule Check (1 поиск на гипотезу).

43. **Saturated market kills доминируют.** v9-run7: 9/20 (45%) убиты по blacklist #11 — meal planning, tab management, gym tracking, meditation, content scheduling, expense splitting, read-it-later. Generator продолжает генерировать в зрелых рынках несмотря на промпт. Исправлено в v10: расширен список saturated categories с 6 до 14 конкретных категорий с конкурентами.

44. **100% kill rate = проблема на входе, не на фильтре.** v9-run7: 20/20 убиты (13 Rule Check + 7 Critic). Critic и Rule Check работают правильно — находят реальных конкурентов и бесплатные альтернативы. Проблема в качестве input: Generator получает устаревшие сигналы и генерирует в уже решённых нишах. v10 фокус: input quality через Scout freshness и Competition pre-screen.

45. **Free Alt Pre-screen ловит категорию, не продукт.** v9-run7: Pre-screen поймал 3/10 free alt kills (Actual Budget, Tally, PostHog). Critic поймал оставшиеся 7 (Pocket Casts free, Libib free, Wave free, NormCap free, Spotify for Creators free, Notch free). Причина: Pre-screen ищет "[category] free alternative", а нишевые бесплатные продукты требуют поиска по конкретному job. Competition Pre-screen v10 дополняет Free Alt.

### Из v10-run1 и v10-run2

46. **Competition Pre-screen: Sonnet >> Haiku.** v10-run1 (Haiku): 90% kill rate, false positives (cloud transcribers =/= local transcription, practice suites $39 =/= lightweight memory $12). v10-run2 (Sonnet): 65% kill rate, точнее оценивает job overlap. Haiku соответствует по категории, Sonnet — по конкретному job. Исправлено в v11: Competition Pre-screen всегда на Sonnet.

47. **Пустой прогон = потерянные деньги и 0 знаний.** 2 прогона v10 по ~$1-2 каждый, 0 финалистов. Лучшие гипотезы (H8 SeasonPass, H6 Creator Finance Sync) содержали рыночные инсайты, но были просто убиты без анализа. WEAK-досье с разбором "почему слабая и что нужно чтобы стала сильной" — ценнее пустого вывода. Исправлено в v11: Best Available carry-forward (лучший WEAK → Deep Validator с тегом CONDITIONAL).

48. **Scout signal quality = предсказатель результата.** v10-run2: лучший сигнал = T2.5 (статьи + Etsy шаблоны). Ни один сигнал не имел T1/T1-alt potential. Generator не может компенсировать слабый input — он комбинирует сигналы, а не создаёт спрос. Если Scout не нашёл >= 3 сигнала с T1/T1-alt potential — прогон предсказуемо пустой. Исправлено в v11: Scout Signal Quality Gate перед Generator.

### Из v11-run1 (Best Available activated)

49. **Best Available гарантирует output, но не quality.** v11-run1: 1 WEAK (CONDITIONAL) — Best Available activated, H8 ClipDev. Досье с WWNBT создано, но 1.5/4 осей = строительство на quicksand. CONDITIONAL ≠ MODERATE. Best Available решает проблему пустых прогонов, но не проблему слабого input.

50. **Competition Pre-screen нуждается в расширенном query.** v11-run1: Pieces ($47.8M, AI auto-categorization) — прямой конкурент H8 ClipDev — не найден Competition Pre-screen (искал "clipboard manager", Pieces = "developer snippet tool"). Нужно искать по adjacent category names, а не только по primary keyword.

51. **macOS native features = systemic risk.** v11-run1: macOS Tahoe 26 встроил clipboard history в Spotlight — commoditization категории, которую H8 продаёт. Deep Validator нашёл, но Critic и Quick Validator пропустили. Нужен check "does OS already do this?" в Rule Check.

52. **Generator hallucinate features, а не jobs.** v11-run1: Scout нашёл "developer clipboard underserved" (job). Generator трансформировал в "auto-tag by IDE project" (feature). 23 поиска — 0 evidence что кто-то хочет эту feature. Transformation gap: signal → hypothesis теряет evidence grounding. Исправлено в v12: Evidence Anchor (правило 12) маркирует GROUNDED vs SPECULATIVE features.

53. **Scout breadth vs depth.** v2 (2 STRONG) получал конкретные цитаты ("wish there was cheaper Canny"). v11-run1 Scout нашёл абстрактные сигналы ("developer clipboard underserved"). Breadth-first (10-15 поисков → 15-20 сигналов) оптимизирует coverage, но не depth. Depth-first (3 доп. поиска на топовый сигнал) даёт Generator конкретные workaround chains с шагами. Исправлено в v12: Scout-C depth pass.

54. **Spot-check = дешёвая страховка.** v11-run1: Quality Gate прошёл (14/16 T1/T1-alt potential), но при валидации evidence не найден. Gate проверял *потенциал* сигнала, но не *конвертируемость* — найдутся ли results при поиске. 2 поиска за ~2K перед Generator ($0.01) дешевле пустого прогона ($1-2). Исправлено в v12: Spot-check validation.

### Из v12 (evidence grounding)

55. **Scout-C depth добавляет cost без quality.** v12-run1: ~55K tokens (Scout-C + Spot-check) не улучшили Generator output. Workaround chains документируют существующие workarounds, но не помогают Generator создать novel hypotheses в зрелых рынках. Cost/benefit отрицательный.

56. **Evidence Anchor — лучший механизм v12.** 17/20 GROUNDED, H18 DevClipboard маркирован SPECULATIVE (тот же concept что v11 H8 ClipDev). Ловит speculative features И cross-run repeats. Generator становится честнее в атрибуции.

57. **"Gap without demand" — gap ≠ opportunity.** v12-run1: H7 InvoiceChase имеет объективный gap (AP для micro-SMB через Gmail), но 0 людей просят этот продукт. Рынок пуст не потому что никто не додумался, а потому что спрос = 0. Gap validation должна включать demand check.

### Из v13 (Goal Graph)

58. **Goal Graph снижает конкуренцию, но не повышает demand.** v13-run1: Competition Pre-screen kill rate 47% (vs 62.5% v12-run2), Critic kill rate 22% (vs 50%). Но QV kill rate 71% по NO_SIGNAL — PREVIOUS-level гипотезы слишком далеки от прямого job, 0 людей просят эти продукты. Less competitive ≠ more viable.

59. **"Productivity porn" = системный false demand для indie dev tools.** v13-run1: indie devs жалуются на changelogs (H6), decision journals (H14), context briefings (H1) — но не используют инструменты для их решения. Тест: если бесплатная альтернатива = "просто не делать" (не писать changelogs), demand невалиден. Жалобы ≠ WTP.

60. **Platform features kill point solutions.** v13-run1: Practice.do voice notes убил SessionMemory (H5). v11-run1: macOS Spotlight clipboard убил ClipDev (H8). Системный паттерн: платформы добавляют point solution features → standalone product теряет raison d'etre. Rule Check нуждается в "platform expansion check".

---

## Техническое: JSONL extraction

Субагенты (Task tool) не могут писать файлы через Write.
Результаты нужно извлекать из JSONL output:

```python
python3 -c "
import json
agent_id = 'AGENT_ID'  # из output агента
best = ''
with open(f'/private/tmp/claude-501/-Users-i-iii/tasks/{agent_id}.output') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try: obj = json.loads(line)
        except: continue
        msg = obj.get('message', {})
        content = msg.get('content', '')
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get('type') == 'tool_use':
                    if block.get('name') in ('Write', 'SendMessage'):
                        c = block.get('input', {}).get('content', '')
                        if len(c) > len(best): best = c
        elif isinstance(content, str) and len(content) > len(best):
            best = content
if best:
    with open('OUTPUT.md', 'w') as out: out.write(best)
    print(f'Saved: {len(best)} chars')
"
```

> **Когда использовать:** если результат агента обрезан или нужен полный текст.
> В большинстве случаев Lead получает результат напрямую из Task tool output.

---

## Quick Start

```
1. Заполни профиль основателя (секция выше)

2. Обнови Cross-Run Learning (blacklist/whitelist) если есть данные
   из предыдущих прогонов

3. Создай директорию:
   mkdir -p ~/Documents/discovery-b2c-$(date +%Y%m%d)

4. Запусти в Claude Code:
   "Запусти B2C pet-project discovery v12 по методологии из methodology.md.
   Профиль: [вставить].
   Начни с Round 0: Demand Scout."

5. Pipeline v12:
   R0:    2 Scout-а параллельно (workarounds/emerging + FRESHNESS CHECK для старых сигналов)
   R0.5:  SIGNAL QUALITY GATE (Lead: >= 3 сигнала с T1/T1-alt potential? Если нет — перезапуск Scout)
   R0.75: SPOT-CHECK (2 поиска по лучшим сигналам) + SCOUT-C DEPTH PASS (3 поиска x 3-5 сигналов)
   R1:    Generator (20 гипотез, с EVIDENCE ANCHOR: GROUNDED/SPECULATIVE маркировка)
   R1.5:  Rule Check (Lead manual: blacklist, Pattern Cap, Free Alt Pre-screen,
          COMPETITION PRE-SCREEN на Sonnet) + Dedup + Founder-Fit + API Pre-screen
   R2:    2-3 параллельных мини-Critic-а (С поиском! + job overlap check)
   R2.25: Red Team — devil's advocate (structural risks кроме конкуренции)
   R2.5:  Quick Validator — ВСЕГДА (даже для 1 гипотезы, 4 searches, T1-ALT для novel categories)
   R2.75: BEST AVAILABLE CARRY-FORWARD (если 0 survivors — лучший WEAK → Deep Validator)
   R3:    1-2 Deep Validator-а (blocker-first, RED FLAG skip rule)
   R4:    Synthesis (Lead, WWNBT секция для CONDITIONAL)

6. Итог: минимум 1 досье за прогон. Evidence-grounded features через Scout-C + Evidence Anchor.
```
