# Persona Protocol v15 — JTBD-only (Two-Wave Deep Interviews)

Протокол для полного JTBD цикла без стартовых скаутов.
Основан на Mom Test + AJTBD подходе и разделяет discovery и validation
на независимые волны интервью.

Reference prompts: `ajtbd-prompts.md`.

## Core principles

1. Only past behavior
- вопросы только о реальных эпизодах прошлого
- запрещены вопросы про гипотетическую покупку

2. Separate discovery and validation
- Wave A = поиск jobs
- Wave B = независимая проверка shortlist

3. Panel independence
- персоны Wave A не могут использоваться в Wave B

4. Anti-bias mandatory
- финальная валидация только в двухагентном режиме

5. Dual output
- validated jobs
- discovered jobs backlog

6. Русский язык
- Все названия jobs, job statements, цитаты персон, аналитика — на русском
- Персоны говорят по-русски (даже если имя английское)
- Английский только для имён продуктов (Notion, Zapier) и устоявшихся терминов (JTBD, MRR, SaaS)
- Запрещён рунглиш в аналитическом тексте (см. CLAUDE.md → Язык)

## Wave architecture

### Wave A (Discovery)

Цель: найти jobs, которые реально происходят в жизни людей.

Input:
- domain scope
- persona panel A (8-10)

Output:
- raw job candidates
- workaround chains
- switching signals
- adjacent/discovered jobs

### Wave B (Validation)

Цель: проверить shortlisted jobs на независимой панели.

Input:
- shortlisted jobs (8-12)
- persona panel B (8-10, new)

Output:
- validated evidence per job
- weighted score + verdict
- risk register (RAT)

## Persona construction spec

### Required fields

For each persona define:
- role
- age range
- concrete context
- trigger event
- emotional state at point A
- current workaround (steps)
- current spend (time/money)
- switching history
- intent level (HIGH/MEDIUM/LOW)

### Diversity rules

- минимум 3 разные роли
- минимум 3 разные workflow-модели
- минимум 2 churned personas
- intent mix обязателен

### Independence rules

- Panel B must not reuse names, contexts, or incidents from Panel A
- if overlap detected, regenerate persona

## Interview script (universal)

### Block 1: Last incident

- Расскажи про последний раз, когда тебе нужно было [job context].
- Когда это было и что происходило вокруг?
- Что заняло больше времени, чем ожидалось?
- Что в этом процессе тебя раздражало больше всего?

Capture:
- timestamp/context
- job trigger
- cost of failure

### Block 2: Current workaround

- Как ты решаешь это сейчас, пошагово?
- Какие инструменты/люди участвуют?
- Сколько времени и денег это обычно стоит?
- В каком месте процесс ломается?

Capture:
- steps
- tools
- spend
- friction point

### Block 3: Switching behavior

- Вспомни, когда ты последний раз менял инструмент для похожей задачи.
- Что стало триггером смены?
- Что удерживало от смены?
- Что убедило всё-таки переключиться?

Capture:
- switching trigger
- switching barrier
- evidence of willingness to change

### Block 4: Priority under constraints

- На какое улучшение процесса ты реально потратил время за последний месяц?
- Что ты уже пробовал улучшить за последние 30 дней?
- Почему именно это, а не [target problem]?

Capture:
- relative priority
- revealed preference

### Block 5: Adjacent jobs discovery

- Что в этой же области раздражает тебя даже сильнее?
- На что регулярно уходит время, которое хочется вернуть?

Capture:
- discovered jobs
- severity estimate

## Output schema per interview

For each interview return:
- `job_confirmed`: YES/PARTIAL/NO
- `severity`: 1-10
- `frequency`: daily/weekly/monthly/rare
- `current_spend`: value + type
- `switching_trigger`
- `switching_barrier`
- `key_quote`
- `discovered_jobs[]`

## Job synthesis schema (after Wave A)

For each candidate job:
- `job_id`
- `job_statement` (when/want/so-that)
- `who` (segment)
- `context`
- `breadth_signal` (count of personas with YES/PARTIAL)
- `severity_avg`
- `frequency_mode`
- `existing_spend_pattern`
- `alternative_explanation`

## Validation protocol (Wave B)

### Team setup (mandatory)

Use two-agent team per interview stream:
- Agent A: Interviewer (knows target job)
- Agent B: Persona (knows only persona profile)

### Why mandatory

Single-agent interviews tend to inflate ALIVE verdicts by confirmation bias.
Two-agent isolation is the control layer before final synthesis.

### Blocking rule

If Wave B two-agent interviews are not complete:
- mark run as `UNVALIDATED`
- do not publish final ALIVE verdicts

## Scoring model

Weighted score (0-100):
- Breadth x3
- Severity x2
- Frequency x2
- Current Spend x1
- Switching History x1

Verdict:
- ALIVE >= 60
- WEAK 40-59
- KILL < 40

### RAT overlay (required)

Score top risks by `P x I`:
1. Demand fragility
2. Economic segment quality
3. WTP/value capture
4. Unit economics
5. Scale/distribution constraints

Risk interpretation:
- >20: RED FLAG
- 16-20: AMBER
- <=15: ACCEPTABLE

Each RED FLAG must include mitigation test(s).

## Decision rules

1. If Breadth <= 2 in Wave B -> auto KILL.
2. If score >= 60 but has 2+ RED FLAGs -> cap at WEAK until mitigations pass.
3. If score 40-59 and no RED FLAGs -> WEAK with conditional path.
4. If contradiction rate >40% between interviews -> rerun with refreshed panel B.

## Required artifacts

- `round-1-personas-A.md`
- `round-2-interviews-A.md`
- `round-2.5-job-synthesis.md`
- `round-3-personas-B.md`
- `round-4-interviews-B.md`
- `round-4.5-scoring-rat.md`
- `round-5-synthesis.md`
- `interviews/wave-a/*.md` (полные интервью Wave A)
- `interviews/wave-b/*.md` (полные интервью Wave B)

## Context budget protocol

- Полные transcript'ы интервью сохраняются в:
  - `runs/v15-runN/interviews/wave-a/`
  - `runs/v15-runN/interviews/wave-b/`
- В orchestrator-контекст передаётся только summary per interview:
  - 3-5 наблюдений
  - метрики (`job_confirmed`, severity/frequency, spend, switching)
  - до 2 цитат
- Запрещено переносить полный transcript между стадиями.

## Transcript header (mandatory)

Каждый файл интервью начинается с `## Summary`, затем `## Transcript`.
Шаблон по умолчанию: `interview-template.md`.

Filename pattern:
- Wave A: `A-<job_id>-<persona_id>.md`
- Wave B: `B-<job_id>-<persona_id>.md`

Summary fields (минимум):
- `job_confirmed`
- `severity`
- `frequency`
- `current_spend`
- `switching_trigger`
- `switching_barrier`
- `key_points` (3-5)

## Calibration protocol

Before major methodology change:
1. take 5 known hypotheses (mixed outcomes)
2. run full Wave A + Wave B
3. measure separation quality (target >= 4/5 correct ordering)
4. tune thresholds only once per calibration round

## Anti-drift rules

- No prompt edits without DEVLOG entry.
- No more than 3 variable changes per run.
- No manual verdict override without `override_reason`.
- Keep prompts backward-looking; remove future-intent wording.
