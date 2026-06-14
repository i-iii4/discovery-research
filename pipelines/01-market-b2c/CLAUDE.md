# b2c-discovery — мультиагентный поиск B2C-продуктов для solo-разработчика

Методологический проект: пайплайн из LLM-агентов ищет product-market fit гипотезы
на пересечениях JTBD-ниш. Не код, а система промптов + правил + cross-run learning.
Запускается в Claude Code через Task tool.

## Часть экосистемы

Этот пайплайн — `01-market-b2c` в экосистеме `discovery-research` (см. корневой `../../README.md`). Методология лежит здесь, **данные — в общей папке `../../artifacts/`**, разделяемой всеми пайплайнами.

## Расположение артефактов

| Что | Куда писать |
|---|---|
| Работы (jobs) | `../../artifacts/jobs/` (общие для всех пайплайнов) |
| Гипотезы | `../../artifacts/hypotheses/` (общие) |
| Прогоны (round-*, поиски) | `../../artifacts/runs/01-market-b2c/vN/` |
| Лог результатов | `../../artifacts/runs/01-market-b2c/results.md` |
| История изменений | `../../artifacts/runs/01-market-b2c/DEVLOG.md` |
| Досье финалистов (legacy) | `../../artifacts/runs/01-market-b2c/finalists/` |

Везде ниже относительные пути `runs/...`, `results.md`, `DEVLOG.md`, `finalists/` читать относительно `../../artifacts/runs/01-market-b2c/`. Новые гипотезы/работы пишутся в общие `../../artifacts/{hypotheses,jobs}/` с атрибутами frontmatter (`audience: b2c`, `pipeline: market`, `profile`).

## Required reading

- `methodology.md` — пайплайн, промпты всех агентов, правила генерации, blacklist/whitelist, lessons learned. Главный рабочий файл.
- `ARCHITECTURE.md` — обзор пайплайна, стадии, агенты, поток данных.
- `PLAN.md` — план доработок методологии.
- `../../profiles/` — профили основателя (`saas`, `mobile-us`), общие для экосистемы.
- `../../artifacts/runs/01-market-b2c/results.md` — результаты всех запусков, ранжирование, pipeline comparison.
- `../../artifacts/runs/01-market-b2c/DEVLOG.md` — история изменений по версиям.

## Stack

| Технология | Назначение |
|---|---|
| Claude Code | Среда выполнения (Task tool, субагенты) |
| Claude Sonnet | Агенты: Scout, Generator, Critic, Validator, Synthesis |
| Claude Haiku | Quick Validator (дешёвый gate) |
| Web Search | Demand signals, competition check, validation |

## Запуск пайплайна

```
1. Выбрать профиль основателя: ../../profiles/saas.md или ../../profiles/mobile-us.md
2. Создать директорию ../../artifacts/runs/01-market-b2c/vN/
3. В Claude Code: "Запусти market-b2c discovery по methodology.md, профиль <profile>"
4. Артефакты каждого раунда → ../../artifacts/runs/01-market-b2c/vN/
5. Лог результатов → ../../artifacts/runs/01-market-b2c/results.md
6. Гипотезы-финалисты → ../../artifacts/hypotheses/ (атрибуты: pipeline=market, audience=b2c, profile)
```

## Профиль основателя

Профили вынесены в `../../profiles/` (общие для экосистемы). Прогон выбирает один:

- **saas** — исходный: full-stack solo-dev, web/любая платформа, $5K+/мес, 2 недели до MVP, anti-iGaming.
- **mobile-us** — мобильные приложения под рынок США, подписка; расширенная рамка (код — commodity, главный фильтр — органическая дистрибуция без UA-бюджета).

Атрибут `profile` проставляется в frontmatter каждой гипотезы/работы прогона.

## Методологическая культура

Проект строится как воспроизводимая система, а не набор экспериментов.

### Запрещено
- Менять промпты без документирования причины в DEVLOG.md
- Менять больше 3 переменных между запусками (невозможна атрибуция)
- Удалять из blacklist без проверки актуальности
- Добавлять в whitelist паттерн, который выжил только в одном запуске
- Оценивать гипотезы "на глаз" — только через пайплайн

### Обязательно
- Каждое изменение методологии обосновано данными из предыдущих запусков
- Новое правило: сначала описать в PLAN.md, потом внести в methodology.md
- После каждого запуска: обновить results.md, DEVLOG.md, methodology.md (lessons learned)
- Cross-run comparison: таблица в results.md обновляется после каждого запуска

## Style conventions

- Промпты агентов: английский (поисковые запросы) + русский (инструкции)
- Результаты и анализ: русский
- Технические термины (JTBD, demand signal, kill rate): оставлять без перевода
- Длинное тире (—) вместо двойного дефиса

## Documentation maintenance

| Документ | Когда обновлять |
|---|---|
| CLAUDE.md | Изменился стек, профиль основателя, структура проекта |
| ARCHITECTURE.md | Добавлена/убрана стадия пайплайна, изменена роль агента |
| PLAN.md | Задача начата/завершена, новые задачи обнаружены |
| DEVLOG.md | После каждого запуска пайплайна (= одна запись) |
| methodology.md | Изменены промпты, правила, blacklist/whitelist |
| results.md | Добавлены результаты нового запуска |
