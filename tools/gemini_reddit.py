#!/usr/bin/env python3
"""Достаёт Reddit demand-сигналы через Gemini API с Google Search grounding.

Reddit заблокировал robots.txt для всех краулеров кроме Google (лицензионная
сделка). Gemini grounding ходит в индекс Google, поэтому видит Reddit —
это легальный обходной канал для краулера, которому Reddit недоступен напрямую.

Ключ читается из env GEMINI_API_KEY или из ~/.config/discovery-research/gemini.env
(вне git). Внешних зависимостей нет — только стандартная библиотека.

Использование:
    python3 gemini_reddit.py "AI astrology chatbot apps people wish existed"
    python3 gemini_reddit.py "<query>" --raw      # сырой JSON ответа
"""
import os
import sys
import json
import argparse
import urllib.request
import urllib.error

CONFIG = os.path.expanduser("~/.config/discovery-research/gemini.env")


def load_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    if os.path.exists(CONFIG):
        for line in open(CONFIG, encoding="utf-8"):
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit("GEMINI_API_KEY не найден (env или " + CONFIG + ")")


def query_gemini(prompt, key, model):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent"
    )
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {"thinkingConfig": {"thinkingBudget": 0}},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=180)
    except urllib.error.HTTPError as e:
        sys.exit(f"Gemini API error {e.code}: {e.read().decode('utf-8')[:800]}")
    return json.loads(resp.read())


REDDIT_PROMPT = (
    "Search Reddit discussions about: {q}\n\n"
    "Focus ONLY on Reddit (reddit.com) threads. Extract real user DEMAND signals: "
    "complaints about existing apps, 'I wish there was an app that...', repeated "
    "workaround chains, feature requests, willingness-to-pay hints. "
    "For each signal report: subreddit, a short paraphrase of what the user actually said, "
    "approximate engagement if visible (upvotes / comments), and the reddit URL. "
    "Group signals by theme. Do NOT invent — only what is actually found in search results; "
    "if a thread is weak or unverified, say so. Answer in Russian for analysis, keep app names "
    "and quotes in English."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="что искать на Reddit")
    ap.add_argument("--model", default="gemini-2.5-flash")
    ap.add_argument("--raw", action="store_true", help="вывести сырой JSON")
    ap.add_argument("--plain", action="store_true", help="произвольный промпт без Reddit-обёртки")
    args = ap.parse_args()

    key = load_key()
    prompt = args.query if args.plain else REDDIT_PROMPT.format(q=args.query)
    data = query_gemini(prompt, key, args.model)

    if args.raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    try:
        cand = data["candidates"][0]
        text = "".join(p.get("text", "") for p in cand["content"]["parts"])
    except (KeyError, IndexError):
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    print(text)

    gm = cand.get("groundingMetadata", {})
    chunks = gm.get("groundingChunks", [])
    if chunks:
        print("\n--- Источники (grounding) ---")
        for c in chunks:
            web = c.get("web", {})
            print(f"- {web.get('title', '')}: {web.get('uri', '')}")
    queries = gm.get("webSearchQueries", [])
    if queries:
        print("\n--- Поисковые запросы Gemini ---")
        for q in queries:
            print(f"- {q}")


if __name__ == "__main__":
    main()
