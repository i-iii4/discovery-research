# b2c-discovery — мультиагентный поиск B2C-продуктов для solo-разработчика

Методологический проект: пайплайн из LLM-агентов ищет product-market fit гипотезы
на пересечениях JTBD-ниш. Не код, а система промптов + правил + cross-run learning.
Запускается в Claude Code через Task tool.

## Required reading

- `methodology.md` — пайплайн v12, промпты всех агентов, правила генерации, blacklist/whitelist, lessons learned. Главный рабочий файл.
- `results.md` — результаты всех запусков (v1-v10), ранжирование гипотез, pipeline comparison.
- `ARCHITECTURE.md` — обзор пайплайна v12, стадии, агенты, поток данных.
- `PLAN.md` — план доработок методологии.
- `DEVLOG.md` — история изменений по версиям.

## Stack

| Технология | Назначение |
|---|---|
| Claude Code | Среда выполнения (Task tool, субагенты) |
| Claude Sonnet | Агенты: Scout, Generator, Critic, Validator, Synthesis |
| Claude Haiku | Quick Validator (дешёвый gate) |
| Web Search | Demand signals, competition check, validation |

## Structure

```
b2c-discovery/
  CLAUDE.md           — этот файл
  ARCHITECTURE.md     — обзор пайплайна (v12)
  PLAN.md             — план доработок
  DEVLOG.md           — история изменений
  methodology.md      — пайплайн + промпты (главный рабочий файл, v12)
  results.md          — результаты всех запусков
  runs/               — артефакты отдельных запусков
    v7-run1/          — round-0 через round-4
    v7-run2/          — round-0 через round-4
    v8-run1/          — round-0 через round-4
  finalists/          — подробные досье финалистов (14 файлов, Obsidian wikilinks)
    README.md         — индекс всех финалистов + Dataview query
```

## Запуск пайплайна

```
1. Обновить methodology.md (blacklist, whitelist, профиль основателя)
2. Создать директорию runs/vN/
3. В Claude Code: "Запусти B2C pet-project discovery v12 по методологии из methodology.md"
4. Артефакты каждого раунда сохраняются в runs/vN/
5. Финальные результаты добавляются в results.md
6. Досье финалистов (MODERATE/STRONG/CONDITIONAL) создаются в finalists/
```

## Профиль основателя (текущий)

- Стек: full-stack, любая платформа
- Интересные области: Productivity, PKM, AI/LLM, Health/Wellness, Creator tools, SaaS tools
- Anti-области: iGaming
- Целевой доход: $5K+/мес
- Ограничение: 2 недели до MVP, один разработчик

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
