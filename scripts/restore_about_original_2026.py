#!/usr/bin/env python3
"""Restore the About section to its pre-Avito design, preserving all other sections."""
from pathlib import Path
import re

p = Path("index.html")
s = p.read_text(encoding="utf-8")
original = s

def replace_one(pattern, repl, name):
    global s
    matches=list(re.finditer(pattern,s,re.S|re.I))
    if len(matches)!=1:
        raise RuntimeError(f"{name}: expected exactly one match, found {len(matches)}")
    m=matches[0]
    s=s[:m.start()]+repl(m)+s[m.end():]
    print("Restored:",name)

# The original image already includes the old About wording. Return the desktop
# About HTML to its original invisible accessibility-only section.
restore_desktop = '''<section class="screen-reader-only" id="about-desktop" data-panel="about" aria-label="Обо мне">
        <h1>Капитан Смоллет — Богдан, магистр ВШЭ Санкт-Петербург</h1>
        <p>Программист в процессе становления. Люблю математику, машинное обучение и хорошие задачи. Умею разбираться в сложном, доводить дела до конца и работать в команде. Характер спокойный, любознательный.</p>
      </section>'''
replace_one(
    r'<section\s+class="sheet about-visible about-patched"\s+id="about-desktop"\s+data-panel="about"[^>]*>.*?</section>',
    lambda m:restore_desktop,
    "desktop About invisible/illustrated state"
)

# Completely remove the later CSS parchment overlay (it obscures the original artwork).
replace_one(
    r'\n/\* About: the old paragraph was embedded in the original illustration\..*?'
    r'#desktop-main\s+#about-desktop\.about-patched\s+\.about-main-copy\s*\{.*?\}\s*',
    lambda m:"\n",
    "added About parchment overlay CSS"
)

# Restore the initial mobile description too, without altering portraits or name.
old_mobile='''<p class="brief">МАГИСТР ВШЭ СПБ, ПРОГРАММИСТ (В ПРОЦЕССЕ СТАНОВЛЕНИЯ).<br>ЛЮБЛЮ МАТЕМАТИКУ, ML И ХОРОШИЕ ЗАДАЧИ.<br>УМЕЮ РАЗБИРАТЬСЯ В СЛОЖНОМ, ДОВОДИТЬ ДЕЛА ДО КОНЦА И РАБОТАТЬ В КОМАНДЕ.<br>ХАРАКТЕР СПОКОЙНЫЙ, ЛЮБОЗНАТЕЛЬНЫЙ.<br>НЕ ЖЕНАТ.</p>'''
replace_one(
    r'<p\s+class="brief"(?:\s+style="[^"]*")?\s*>.*?</p>',
    lambda m:old_mobile,
    "mobile About original text"
)

# Validate that only About HTML/CSS was edited, and embedded media are untouched.
assert 'about-patched' not in s
assert 'about-main-copy' not in s
assert 'about-visible' not in s
assert 'class="screen-reader-only" id="about-desktop"' in s
assert "МАГИСТР ВШЭ СПБ, ПРОГРАММИСТ" in s
assert 'СТУДЕНТ МАГИСТРАТУРЫ НИУ ВШЭ' not in s[s.index('<main id="desktop-main">'):s.index('data-panel="education"')]
for token in ('data:image/', 'data:audio/', 'data:font/', '<script', 'data-panel="', 'data-panel="education"','mailto:brukhabotov@edu.hse.ru'):
    assert original.count(token)==s.count(token),(token,"changed")
assert len(s)>len(original)*0.98
p.write_text(s,encoding="utf-8")
print("Original About presentation restored; all images, sounds, scripts preserved.")
