#!/usr/bin/env python3
"""Exact approved portfolio text corrections, preserving scripts and media."""
from pathlib import Path
import re

path=Path("index.html")
original=path.read_text(encoding="utf-8")
text=original
about=("Студент магистратуры НИУ ВШЭ, программа „Машинное обучение и анализ данных“. "
       "Интересуюсь математической статистикой, анализом данных и ML. "
       "Развиваюсь в Python, участвую в командных проектах и хочу применять "
       "свои знания для решения реальных продуктовых задач. "
       "Характер спокойный. Любознательный. Не женат.")
contact="Открыт к новому опыту! Для связи — учебная почта!"

def change_once(pattern, replacement, label):
    global text
    matches=list(re.finditer(pattern,text,re.S|re.I))
    if len(matches)!=1:
        raise RuntimeError(f"{label}: expected one match, got {len(matches)}")
    m=matches[0]
    text=text[:m.start()]+replacement(m)+text[m.end():]
    print("Updated:",label)

desktop=f"""<section class="sheet about-visible" id="about-desktop" data-panel="about" aria-label="Обо мне">
        <p class="sheet-kicker">ЛИЧНОЕ ДЕЛО / ЛИСТ I</p>
        <h1>КАПИТАН СМОЛЛЕТ</h1>
        <p>{about}</p>
      </section>"""
change_once(r'<section\s+class="(?:screen-reader-only|sheet(?: about-visible)?)"\s+id="about-desktop"\s+data-panel="about"[^>]*>.*?</section>',
            lambda m:desktop,"desktop about; visible in the parchment layout")
change_once(r'<p\s+class="brief"[^>]*>.*?</p>',
            lambda m:'<p class="brief" style="font:600 1.12rem/1.48 Arial,sans-serif;text-transform:none">'+about+'</p>',
            "mobile about")
old_note="Уровни навыков не преувеличены: портфолио растёт вместе с опытом."
change_once(r'\s*<p class="note">'+re.escape(old_note)+r'</p>',
            lambda m:"","remove unwanted skills note")
change_once(r'(<h1 id="skills-title">.*?</h1>\s*<p>).*?(</p>)',
            lambda m:m[1]+"Инструменты анализа данных и разработки."+m[2],
            "concise skills intro")
change_once(r'(<h1 id="contacts-title">.*?</h1>\s*<p>).*?(</p>)',
            lambda m:m[1]+contact+m[2],"contacts intro")

assert text.count(about)==2
assert text.count(contact)==1
assert old_note not in text
assert "Уровни указаны без преувеличений" not in text
assert "mailto:brukhabotov@edu.hse.ru" in text
assert 'data-panel="education"' in text and 'data-panel="projects"' in text
assert "diploma-agu-public.webp" not in text
for token in ('<script','data:audio','data:image','data-panel="'):
    assert text.count(token)==original.count(token),(token,"media/script count changed")
assert len(text) > len(original)*0.98
path.write_text(text,encoding="utf-8")
print("Verified HTML edits",len(original),"->",len(text))
