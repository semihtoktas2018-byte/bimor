# -*- coding: utf-8 -*-
# Tum sayfalara sabit (floating) WhatsApp butonu ekler + ana sayfadaki bos
# wa.me linklerine BIMOR mesaji koyar. Repo kokunde: python3 add_whatsapp.py
import glob, os

TXT="Merhaba%20BIMOR%2C%20%C3%BCr%C3%BCnleriniz%20hakk%C4%B1nda%20bilgi%20almak%20istiyorum."
WA=f"https://wa.me/905446452430?text={TXT}"

CSS_BTN = f'''<style>
.wa-float{{position:fixed;right:22px;bottom:22px;width:60px;height:60px;border-radius:50%;
background:#25D366;display:flex;align-items:center;justify-content:center;z-index:9999;
box-shadow:0 8px 26px rgba(37,211,102,.45);transition:transform .25s}}
.wa-float:hover{{transform:scale(1.08)}}
.wa-float svg{{width:32px;height:32px;fill:#fff}}
.wa-float::after{{content:"";position:absolute;inset:0;border-radius:50%;
box-shadow:0 0 0 0 rgba(37,211,102,.5);animation:waPulse 2.2s infinite}}
@keyframes waPulse{{0%{{box-shadow:0 0 0 0 rgba(37,211,102,.5)}}70%{{box-shadow:0 0 0 16px rgba(37,211,102,0)}}100%{{box-shadow:0 0 0 0 rgba(37,211,102,0)}}}}
@media(max-width:600px){{.wa-float{{width:54px;height:54px;right:16px;bottom:16px}}.wa-float svg{{width:28px;height:28px}}}}
</style>'''

BTN = f'''<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp ile yaz">
<svg viewBox="0 0 24 24"><path d="M17.5 14.4c-.3-.15-1.77-.87-2.04-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-1.77-.88-2.93-1.57-4.1-3.57-.31-.53.31-.5.88-1.65.1-.2.05-.37-.02-.52-.08-.15-.67-1.6-.92-2.2-.24-.58-.49-.5-.67-.5h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.1 3.2 5.08 4.49 2.98 1.28 2.98.85 3.52.8.53-.05 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35M12 2a10 10 0 00-8.6 15.1L2 22l4.98-1.3A10 10 0 1012 2"/></svg>
</a>'''

def process(f):
    t=open(f,encoding='utf-8').read(); ch=False
    # 1) bos wa.me linklerine BIMOR metni ekle (float butondan once)
    if 'https://wa.me/905446452430"' in t:
        t=t.replace('https://wa.me/905446452430"', WA+'"'); ch=True
    # 2) floating buton (yoksa)
    if 'wa-float' not in t:
        t=t.replace('</body>', CSS_BTN+'\n'+BTN+'\n</body>',1); ch=True
    if ch: open(f,'w',encoding='utf-8').write(t)
    print(('+ ' if ch else '. ')+f)

if not os.path.exists('index.html'):
    raise SystemExit('repo kokunde calistir')
for f in sorted(glob.glob('*.html')): process(f)
print('WhatsApp butonu TAMAM')
