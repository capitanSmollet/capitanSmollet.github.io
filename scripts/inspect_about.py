from pathlib import Path
import re
s=Path("index.html").read_text()
print("LENGTH",len(s))
print("DISPLAY TYPE",len(re.findall(r'data:image/',s)),len(re.findall(r'data:audio/',s)))
s=re.sub(r'data:(?:image|audio)/[^)"\s>]+', '[EMBEDDED_MEDIA]',s)
print("HTML/CSS first 14000\n",s[:14000])
for key in ['about-visible','about-desktop','class="brief"','id="desktop-main"','class="scene"','class="mobile-layout"','background-image','@media','hotspot-nav']:
 print("\n\nKEY",key)
 for m in list(re.finditer(re.escape(key),s))[:4]:
  print(s[max(0,m.start()-650):m.start()+1200])
