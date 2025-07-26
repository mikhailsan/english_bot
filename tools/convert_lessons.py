# tools/convert_lessons.py
# Превращает lessons.txt (формат: "word — перевод | example | пример")
# в lessons.json для бота.

import json, pathlib, re, sys

src = pathlib.Path("data/lessons.txt")
dst = pathlib.Path("data/lessons.json")

if not src.exists():
    sys.exit(f"Файл {src} не найден!")

lessons = []
with src.open(encoding="utf8") as f:
    for n, line in enumerate(f, 1):
        line = line.strip()
        if not line or '—' not in line or '|' not in line:
            continue

        # делим:  слово — перевод | пример | пример_рус
        parts = re.split(r"\s*—\s*|\s*\|\s*", line)
        if len(parts) != 4:
            print(f"⚠️  Строка {n} пропущена (не 4 части): {line}")
            continue

        en, ru, ex, ex_ru = [p.strip() for p in parts]
        lessons.append({
            "en": en,
            "ru": ru,
            "example": ex,
            "example_ru": ex_ru
        })

if not lessons:
    sys.exit("❌ Не удалось разобрать ни одной строки.")

dst.write_text(json.dumps(lessons, ensure_ascii=False, indent=2),
               encoding="utf8")
print(f"✅ Готово! Записано {len(lessons)} слов в {dst}")
