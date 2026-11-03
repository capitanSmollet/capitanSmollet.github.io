#!/usr/bin/env python3
"""Fix desktop About: place the new text BELOW portraits on an opaque parchment patch."""
from pathlib import Path
import re

path=Path("index.html")
original=path.read_text(encoding="utf-8")
s=original
about=("Студент магистратуры НИУ ВШЭ, программа «Машинное обучение и анализ данных». "
       "Интересуюсь математической статистикой, анализом данных и ML. "
       "Развиваюсь в Python, участвую в командных проектах и хочу применять "
       "свои знания для решения реальных продуктовых задач. "
       "Характер спокойный. Любознательный. Не женат.")
section=(
'<section class="sheet about-visible about-patched" id="about-desktop" data-panel="about" aria-label="Обо мне">'
'<p class="about-main-copy">'+about+'</p>'
'</section>'
)
pattern=r'<section\s+class="sheet about-visible"\s+id="about-desktop"\s+data-panel="about"[^>]*>.*?</section>'
matches=list(re.finditer(pattern,s,re.S))
assert len(matches)==1,f"Expected one upper text overlay, got {len(matches)}"
m=matches[0]
s=s[:m.start()]+section+s[m.end():]
css="""
/* About: the old paragraph was embedded in the original illustration.
   Place a parchment panel ONLY over its lower text area, leaving portraits untouched.
   The panel contains the current, editable HTML text. */
#desktop-main #about-desktop.about-patched {
  display:block;
  position:absolute;
  top:47.2%;
  left:6.5%;
  width:87.2%;
  height:33.6%;
  z-index:5;
  overflow:hidden;
  padding:1.9cqw 2.0cqw;
  border:0;
  box-shadow:none;
  border-radius:0;
  background:
    repeating-linear-gradient(90deg,transparent 0 16.1cqw,rgba(128,103,63,.075) 16.1cqw 16.2cqw),
    repeating-linear-gradient(0deg,transparent 0 6.8cqw,rgba(128,103,63,.07) 6.8cqw 6.9cqw),
    linear-gradient(110deg,#f0dfb9,#efddb3 60%,#ecdaad);
  -webkit-mask-image:linear-gradient(to bottom,transparent 0,black 3%,black 96%,transparent 100%);
  mask-image:linear-gradient(to bottom,transparent 0,black 3%,black 96%,transparent 100%);
  animation:none;
}
#desktop-main #about-desktop.about-patched .about-main-copy {
  margin:0;
  padding:.3cqw 0;
  font-family:Captain,Impact,"Arial Narrow",sans-serif;
  font-size:2.05cqw;
  font-weight:400;
  line-height:1.23;
  text-transform:uppercase;
  color:#1e1710;
  letter-spacing:.01em;
  text-shadow:none;
  overflow-wrap:break-word;
}
"""
assert "/* About: the old paragraph was embedded" not in s
assert s.count("</style>")==1
s=s.replace("</style>",css+"\n</style>",1)
# Keep existing mobile text, animation, images/audio and all other sections intact.
assert s.count(about)>=1
assert "class=\"sheet about-visible about-patched\"" in s
assert "Уровни навыков не преувеличены" not in s
assert "Открыт к новому опыту! Для связи — учебная почта!" in s
assert "mailto:brukhabotov@edu.hse.ru" in s
assert "diploma-agu-public.webp" not in s
for token in ("data:image/","data:audio/","data:font/","<script","data-panel="):
    assert s.count(token)==original.count(token),(token,"count changed")
assert len(s)>len(original)*.98
path.write_text(s,encoding="utf-8")
print("Repositioned About below the portraits. Original media and other panels preserved.")
