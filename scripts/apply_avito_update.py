#!/usr/bin/env python3
# Site content update: Avito Product Analyst application. No media or JS changes.
import pathlib, re, html, sys
p=pathlib.Path("index.html")
s=p.read_text(encoding="utf-8")
old=s
changes=[]
def swap(pattern, repl, label):
    global s
    hits=list(re.finditer(pattern,s,re.S|re.I))
    if len(hits)!=1:
        raise RuntimeError(f"{label}: expected 1 occurrence, found {len(hits)}")
    s=s[:hits[0].start()]+repl(hits[0])+s[hits[0].end():]
    changes.append(label)
def section(panel, mapper):
    pat=rf'(<section\b(?=[^>]*class="sheet")(?=[^>]*data-panel="{panel}")[^>]*>)(.*?)(</section>)'
    swap(pat,lambda m:m[1]+mapper(m[2])+m[3],f"section {panel}")
def single(t,pattern,repl,label):
    hits=list(re.finditer(pattern,t,re.S|re.I))
    if len(hits)!=1: raise RuntimeError(f"{label}: expected 1 occurrence, found {len(hits)}")
    m=hits[0]
    return t[:m.start()]+repl(m)+t[m.end():]
about="Студент магистратуры НИУ ВШЭ по программе «Машинное обучение и анализ данных». Интересуюсь математической статистикой, анализом данных и ML. Развиваюсь в Python, участвую в командных проектах и хочу применять свои знания для решения реальных продуктовых задач."
mobile="СТУДЕНТ МАГИСТРАТУРЫ НИУ ВШЭ · «МАШИННОЕ ОБУЧЕНИЕ И АНАЛИЗ ДАННЫХ».<br>ИНТЕРЕСУЮСЬ МАТЕМАТИЧЕСКОЙ СТАТИСТИКОЙ, АНАЛИЗОМ ДАННЫХ И ML.<br>РАЗВИВАЮСЬ В PYTHON, УЧАСТВУЮ В КОМАНДНЫХ ПРОЕКТАХ.<br>ХОЧУ ПРИМЕНЯТЬ ЗНАНИЯ ДЛЯ РЕШЕНИЯ РЕАЛЬНЫХ ПРОДУКТОВЫХ ЗАДАЧ."
swap(r'(<section\b[^>]*id="about-desktop"[^>]*>\s*<h1>).*?(</h1>\s*<p>).*?(</p>)',lambda m:m[1]+"Богдан Ухаботов — магистрант НИУ ВШЭ, анализ данных и ML"+m[2]+about+m[3],"About desktop")
swap(r'(<p\s+class="brief">).*?(</p>)',lambda m:m[1]+mobile+m[2],"About mobile")
def education(t):
    if 'data-avito-diploma=' in t:
        return single(t,r'<article class="education-item education-item--diploma" data-avito-diploma="true">.*?</article>',lambda m:card.strip(),"Remove diploma picture")
    return single(t,r'(?=<article\s+class="education-item"[^>]*>\s*<span[^>]*>[^<]*БАКАЛАВРИАТ)',lambda m:card+"\n","AGU education")
card='''\n        <article class="education-item education-item--diploma" data-avito-diploma="true">
          <span class="eyebrow">2026 · ПРОФЕССИОНАЛЬНАЯ ПЕРЕПОДГОТОВКА</span>
          <h2>АДЫГЕЙСКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ</h2>
          <p>Программа «Применение анализа данных в бизнес-процессах». Присвоена квалификация «Специалист по большим данным».</p>
        </article>'''
section("education",education)
def skills(t):
    t=single(t,r'(<h1\s+id="skills-title">.*?</h1>\s*<p>).*?(</p>)',lambda m:m[1]+"Инструменты анализа данных и разработки. Уровни указаны без преувеличений."+m[2],"skills intro")
    categories={
      'ПРОГРАММИРОВАНИЕ':(['Python','SQL · базовый','Git / GitHub','UNIX / терминал','unittest'],'Python — учебные задачи и командная разработка. SQL — базовый уровень; Git, pull request и автотесты — на практике.'),
      'МАТЕМАТИКА':(['Математическая статистика','Теория вероятностей','Линейная алгебра','Мат. анализ'],'Статистические методы применяю в учебных исследованиях распределений и оценок.'),
      'ДАННЫЕ И ML':(['NumPy','SciPy','Matplotlib','KDE','Квантили'],'Анализ выборок, оценивание плотности, работа с квантилями и визуализация. ML продолжаю изучать.')
    }
    for category,(tags,desc) in categories.items():
        pat=rf'(<article\s+class="skills-group">\s*<h2>[^<]*{re.escape(category)}</h2>\s*<div\s+class="skill-tags">).*?(</div>\s*<p>).*?(</p>\s*</article>)'
        t=single(t,pat,lambda m:m[1]+''.join("<span>"+html.escape(x)+"</span>" for x in tags)+m[2]+desc+m[3],"skills "+category)
    return t
section("skills",skills)
def projects(t):
    updates={
     'AI-АГЕНТ ДЛЯ ML':'В команде хакатона Альфа-Банка разработал валидатор предсказаний <code>submission.csv</code> (структура, пропуски, ID, дубликаты); написал автоматические тесты и участвовал в разработке исполнителя Python-кода. <a href="https://github.com/CfHSE/AF-hacaton-AutoML" target="_blank" rel="noopener noreferrer">Код проекта на GitHub</a>.',
     'СТАТИСТИЧЕСКИЕ ЭКСПЕРИМЕНТЫ':'Исследовал нормальное и равномерное распределения на выборках разных размеров: сравнивал гистограммы и KDE с теоретическими плотностями, вычислял квантили выборки и оценок, строил и анализировал графики.'
    }
    for name,desc in updates.items():
        t=single(t,rf'(<h2>\s*{re.escape(name)}\s*</h2>\s*<p>).*?(</p>)',lambda m:m[1]+desc+m[2],"project "+name)
    return t
section("projects",projects)
email="brukhabotov@edu.hse.ru"
def contacts(t):
    t=single(t,r'(<h1\s+id="contacts-title">.*?</h1>\s*<p>).*?(</p>)',lambda m:m[1]+"Открыт к стажировке в продуктовой аналитике и задачам на стыке данных, статистики и ML. Для связи — учебная почта или GitHub."+m[2],"contacts intro")
    if "mailto:"+email not in t:
        link=f'<a class="contact-link" href="mailto:{email}"><span>✉ {email}</span><span aria-hidden="true">↗</span></a>'
        t=single(t,r'(<a\s+class="contact-link"[^>]+href="https://github\.com/capitanSmollet".*?</a>)',lambda m:m[1]+"\n        "+link,"Email link")
    t=t.replace("<p>Другие способы связи добавлю, когда решу, какие контакты хочу сделать публичными.</p>","<p>Открыт к интересным проектам и профессиональному общению.</p>")
    return t
section("contacts",contacts)
swap(r'(<small>ПИРАТСКОЕ ПОРТФОЛИО · )[^<]*(</small>)',lambda m:m[1]+"PYTHON / SQL / ДАННЫЕ"+m[2],"mobile header")
# Only existing metadata, if present.
for key,desc in [('name="description"','Богдан Ухаботов — студент магистратуры НИУ ВШЭ, анализ данных и ML. Python, базовый SQL, математическая статистика. Открыт к стажировке продуктового аналитика.'),('property="og:description"','Портфолио Богдана Ухаботова: анализ данных, Python, статистика и проекты. Продуктовая аналитика и ML.')]:
    pattern=rf'(<meta\s+{re.escape(key)}\s+content=")[^"]*(")'
    if re.search(pattern,s,re.S|re.I):
        swap(pattern,lambda m:m[1]+html.escape(desc,quote=True)+m[2],"meta "+key)
# Normalize whitespace-only lines only within the edited Education section.
start=s.index('data-panel="education"')
end=s.index('</section>', start)
s=s[:start]+re.sub(r'(?m)^[ \\t]+
assert s!=old and 'SQL · базовый' in s and 'mailto:'+email in s
assert '<img' not in re.search(r'<article class="education-item education-item--diploma".*?</article>',s,re.S)[0]
p.write_text(s,encoding="utf-8")
print("Updated sections:",", ".join(changes),"bytes:",len(old.encode()),"->",len(s.encode()))
, '', s[start:end])+s[end:]
# Verify all changes before writing.
assert s!=old and 'SQL · базовый' in s and 'mailto:'+email in s
assert '<img' not in re.search(r'<article class="education-item education-item--diploma".*?</article>',s,re.S)[0]
p.write_text(s,encoding="utf-8")
print("Updated sections:",", ".join(changes),"bytes:",len(old.encode()),"->",len(s.encode()))
