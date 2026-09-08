#!/usr/bin/env python3
# BIMOR PR1 build — repo kokunde calistir: python3 build_pr1.py
# Yapar: og-image.jpg uretir + tum sayfalara OG/Twitter/schema, ortak footer
# (imza+2026+2 adres+teslimat bolgeleri), de/ru dil CSS'i, ve index'e lojistik
# avantaj bolumu. Idempotent: tekrar calistirmak zarar vermez.
import re, glob, os, sys, subprocess

SITE = "https://bimor.store"
OG = {'alex':'alex-hero.jpg','aslan-throne':'aslan-throne.jpg','bagdat':'bagdat-hero.jpg',
'hanedan':'hanedan-hero.jpg','milano':'milano-hero.jpg','sahmaran':'sahmaran-hero.jpg',
'sumen':'sumen-chaise.jpg','varna':'varna-hero.jpg','vezir':'vezir-rocking.jpg',
'zera':'zera-hero.jpg','index':'og-image.jpg'}

# ---------- 1) OG IMAGE ----------
def build_og():
    if os.path.exists('og-image.jpg'):
        print('og-image.jpg zaten var, atlandi'); return
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageEnhance
    except ImportError:
        print('Pillow yok, kuruluyor...')
        subprocess.run([sys.executable,'-m','pip','install','pillow','-q','--break-system-packages'],check=False)
        try:
            from PIL import Image, ImageDraw, ImageFont, ImageEnhance
        except ImportError:
            import shutil; shutil.copy('bagdat-hero.jpg','og-image.jpg')
            print('UYARI: Pillow kurulamadi, bagdat-hero.jpg og-image olarak kopyalandi'); return
    W,H=1200,630
    base=Image.open('bagdat-hero.jpg').convert('RGB')
    bw,bh=base.size; s=max(W/bw,H/bh); base=base.resize((int(bw*s),int(bh*s)),Image.LANCZOS)
    bw,bh=base.size; l=(bw-W)//2; t=(bh-H)//2; base=base.crop((l,t,l+W,t+H))
    base=ImageEnhance.Color(base).enhance(1.05); base=ImageEnhance.Brightness(base).enhance(0.82)
    grad=Image.new('L',(W,H),0); gd=ImageDraw.Draw(grad)
    for y in range(H): gd.line([(0,y),(W,y)],fill=int(150*(y/H)**1.3))
    base=Image.composite(Image.new('RGB',(W,H),(10,8,6)),base,grad)
    d=ImageDraw.Draw(base); GOLD=(196,163,90); GOLDL=(223,192,122); CREAM=(250,248,243); m=28
    d.rectangle([m,m,W-m,H-m],outline=GOLD,width=2)
    def fnt(sz,bold=True):
        for p in (['/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'] if bold else ['/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf']):
            if os.path.exists(p): return ImageFont.truetype(p,sz)
        return ImageFont.load_default()
    def ctext(y,txt,f,fill,ls=0):
        if ls:
            ws=[d.textlength(c,font=f) for c in txt]; tot=sum(ws)+ls*(len(txt)-1); x=(W-tot)/2
            for c,w in zip(txt,ws): d.text((x,y),c,font=f,fill=fill); x+=w+ls
        else:
            d.text(((W-d.textlength(txt,font=f))/2,y),txt,font=f,fill=fill)
    ctext(232,"LUXURY FURNITURE  ·  İNEGÖL",fnt(22,False),GOLDL,6)
    ctext(268,"BIMOR",fnt(140,True),CREAM,10)
    ctext(430,"Özel Üretim · Toptan · İhracat",fnt(30,False),CREAM)
    ctext(480,"Avrupa · Orta Doğu · Rusya",fnt(24,False),GOLDL,2)
    ctext(540,"bimor.store",fnt(26,True),GOLD,4)
    base.save('og-image.jpg','JPEG',quality=86,optimize=True); print('og-image.jpg uretildi')

# ---------- 2) HEAD (OG + schema) ----------
JSONLD='''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FurnitureStore",
  "name": "BIMOR Luxury Furniture",
  "url": "https://bimor.store",
  "image": "https://bimor.store/og-image.jpg",
  "logo": "https://bimor.store/og-image.jpg",
  "description": "Inegol merkezli luks mobilya markasi. Ozel uretim, toptan satis ve ihracat. Avrupa, Orta Dogu ve Rusya'ya teslimat.",
  "telephone": "+90 544 645 24 30",
  "priceRange": "$$$",
  "address": {"@type":"PostalAddress","streetAddress":"Yenice Mah.","addressLocality":"Inegol","addressRegion":"Bursa","addressCountry":"TR"},
  "location": [
    {"@type":"Place","name":"Tasarim & Uretim Merkezi","address":{"@type":"PostalAddress","streetAddress":"Yenice Mah.","addressLocality":"Inegol","addressRegion":"Bursa","addressCountry":"TR"}},
    {"@type":"Place","name":"Merkez Ofis & Lojistik","address":{"@type":"PostalAddress","streetAddress":"Bursa Gida Toptancilari Sitesi","addressLocality":"Nilufer","addressRegion":"Bursa","addressCountry":"TR"}}
  ],
  "areaServed": ["Turkiye","Bulgaristan","Romanya","Yunanistan","Karadag","Suudi Arabistan","BAE","Katar","Kuveyt","Urdun","Iran","Rusya"],
  "sameAs": ["https://instagram.com/bimor_store","https://facebook.com/profile.php?id=61575530913797","https://wa.me/905446452430"]
}
</script>'''

def head_block(slug,title,desc):
    img=f"{SITE}/{OG[slug]}"; url=f"{SITE}/" if slug=='index' else f"{SITE}/{slug}.html"
    t=title.replace('"','&quot;'); dd=desc.replace('"','&quot;')
    return f'''<!-- OG / Social -->
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="BIMOR Luxury Furniture">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{dd}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="tr_TR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{dd}">
<meta name="twitter:image" content="{img}">
{JSONLD}
'''

# ---------- 3) FOOTER (dogru surum: .bf-adr strong'da display:block YOK) ----------
FOOTER = r'''<style>
.bamir-ft{background:var(--bl);color:var(--cr);padding:64px 80px 28px;font-family:'Didact Gothic',sans-serif;position:relative;z-index:2}
.bamir-ft a{color:var(--cr);text-decoration:none;transition:color .3s}
.bamir-ft a:hover{color:var(--gl)}
.bamir-ft .bf-top{display:grid;grid-template-columns:1.4fr 1fr 1.2fr 1fr;gap:44px;max-width:1400px;margin:0 auto;padding-bottom:44px;border-bottom:1px solid var(--br)}
.bamir-ft .bf-b{font-family:'Bodoni Moda',serif;font-size:30px;letter-spacing:6px;color:var(--wh)}
.bamir-ft .bf-s{font-size:11px;letter-spacing:4px;text-transform:uppercase;color:var(--g);margin:6px 0 16px}
.bamir-ft .bf-tag{font-size:14px;line-height:1.7;color:var(--md);max-width:320px}
.bamir-ft .bf-soc{display:flex;gap:14px;margin-top:18px;font-size:18px}
.bamir-ft h5{font-size:11px;letter-spacing:3px;text-transform:uppercase;color:var(--g);margin-bottom:16px}
.bamir-ft ul{list-style:none}
.bamir-ft li{margin-bottom:9px;font-size:14px}
.bamir-ft .bf-adr{font-size:13px;line-height:1.6;color:var(--md);margin-bottom:16px}
.bamir-ft .bf-adr strong{color:var(--cr);font-size:12px;letter-spacing:1px;margin-bottom:3px}
.bamir-ft .bf-reg{font-size:13px;line-height:1.7;color:var(--md)}
.bamir-ft .bf-reg strong{color:var(--gl);font-weight:400}
.bamir-ft .bf-bot{max-width:1400px;margin:26px auto 0;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;font-size:12px;color:var(--md)}
.bamir-ft .bf-sig{letter-spacing:3px;text-transform:uppercase;font-size:10px;color:var(--gd)}
.bamir-ft .bf-sig b{color:var(--g);font-weight:700}
@media(max-width:860px){.bamir-ft{padding:48px 22px 22px}.bamir-ft .bf-top{grid-template-columns:1fr 1fr;gap:32px}.bamir-ft .bf-bot{flex-direction:column;text-align:center}}
</style>
<footer class="bamir-ft">
  <div class="bf-top">
    <div>
      <div class="bf-b">BIMOR</div>
      <div class="bf-s">Luxury Furniture</div>
      <p class="bf-tag" data-tr>Inegol'den dunyaya - ozel uretim, toptan satis ve ihracat. Avrupa, Orta Dogu ve Rusya'ya guvenli teslimat.</p>
      <p class="bf-tag" data-en>From Inegol to the world - custom production, wholesale & export. Safe delivery to Europe, the Middle East and Russia.</p>
      <p class="bf-tag" data-ar>من إينيغول إلى العالم - إنتاج مخصص وبيع بالجملة وتصدير. توصيل آمن إلى أوروبا والشرق الأوسط وروسيا.</p>
      <p class="bf-tag" data-de>Von Inegol in die Welt - Massfertigung, Grosshandel & Export. Sichere Lieferung nach Europa, in den Nahen Osten und nach Russland.</p>
      <div class="bf-soc">
        <a href="https://wa.me/905446452430" target="_blank" aria-label="WhatsApp">&#128172;</a>
        <a href="https://instagram.com/bimor_store" target="_blank" aria-label="Instagram">&#128247;</a>
        <a href="https://facebook.com/profile.php?id=61575530913797" target="_blank" aria-label="Facebook">&#128100;</a>
      </div>
    </div>
    <div>
      <h5 data-tr>Adreslerimiz</h5><h5 data-en>Our Locations</h5><h5 data-ar>عناويننا</h5><h5 data-de>Unsere Standorte</h5>
      <div class="bf-adr">
        <strong data-tr>Tasarim & Uretim Merkezi</strong><strong data-en>Design & Production Center</strong><strong data-ar>مركز التصميم والإنتاج</strong><strong data-de>Design- & Produktionszentrum</strong>
        Yenice Mah., Inegol / Bursa
      </div>
      <div class="bf-adr">
        <strong data-tr>Merkez Ofis & Lojistik</strong><strong data-en>Head Office & Logistics</strong><strong data-ar>المكتب الرئيسي واللوجستيات</strong><strong data-de>Hauptburo & Logistik</strong>
        Bursa Gida Toptancilari Sitesi, Nilufer / Bursa
      </div>
    </div>
    <div>
      <h5 data-tr>Teslimat Bolgeleri</h5><h5 data-en>Delivery Regions</h5><h5 data-ar>مناطق التوصيل</h5><h5 data-de>Lieferregionen</h5>
      <div class="bf-reg" data-tr><strong>Avrupa:</strong> Bulgaristan &middot; Romanya &middot; Yunanistan &middot; Karadag<br><strong>Orta Dogu:</strong> S. Arabistan &middot; BAE &middot; Katar &middot; Kuveyt &middot; Urdun &middot; Iran<br><strong>Rusya:</strong> Moskova & Rusya geneli</div>
      <div class="bf-reg" data-en><strong>Europe:</strong> Bulgaria &middot; Romania &middot; Greece &middot; Montenegro<br><strong>Middle East:</strong> Saudi Arabia &middot; UAE &middot; Qatar &middot; Kuwait &middot; Jordan &middot; Iran<br><strong>Russia:</strong> Moscow & across Russia</div>
      <div class="bf-reg" data-ar dir="rtl"><strong>أوروبا:</strong> بلغاريا &middot; رومانيا &middot; اليونان &middot; الجبل الأسود<br><strong>الشرق الأوسط:</strong> السعودية &middot; الإمارات &middot; قطر &middot; الكويت &middot; الأردن &middot; إيران<br><strong>روسيا:</strong> موسكو وجميع أنحاء روسيا</div>
      <div class="bf-reg" data-de><strong>Europa:</strong> Bulgarien &middot; Rumanien &middot; Griechenland &middot; Montenegro<br><strong>Naher Osten:</strong> Saudi-Arabien &middot; VAE &middot; Katar &middot; Kuwait &middot; Jordanien &middot; Iran<br><strong>Russland:</strong> Moskau & russlandweit</div>
    </div>
    <div>
      <h5 data-tr>Iletisim</h5><h5 data-en>Contact</h5><h5 data-ar>تواصل</h5><h5 data-de>Kontakt</h5>
      <ul>
        <li><a href="https://wa.me/905446452430" target="_blank">+90 544 645 24 30</a></li>
        <li><a href="https://instagram.com/bimor_store" target="_blank">@bimor_store</a></li>
        <li><a href="https://facebook.com/profile.php?id=61575530913797" target="_blank">Facebook</a></li>
        <li><a href="https://bimor.store">bimor.store</a></li>
      </ul>
    </div>
  </div>
  <div class="bf-bot">
    <span>&copy; 2026 BIMOR Luxury Furniture. <span data-tr>Tum haklari saklidir.</span><span data-en>All rights reserved.</span><span data-ar>جميع الحقوق محفوظة.</span><span data-de>Alle Rechte vorbehalten.</span></span>
    <span class="bf-sig">A <b>BAMIR ONLINE STORE'S</b> PRODUCTION</span>
  </div>
</footer>'''

# ---------- 4) de/ru dil CSS ----------
CSSINJECT="""/*i18n-de-ru*/
[data-de],[data-ru]{display:none}
[data-lang="de"] [data-de]{display:block}[data-lang="ru"] [data-ru]{display:block}
[data-lang="de"] span[data-de]{display:inline}[data-lang="ru"] span[data-ru]{display:inline}
"""

# ---------- 5) Lojistik avantaj bolumu (index) ----------
LOGI = r'''<!-- LOGISTICS ADVANTAGE -->
<style>
.blog-s{background:var(--bl);color:var(--cr);padding:110px 80px;position:relative;z-index:2;overflow:hidden}
.blog-s .blog-eye{font-size:12px;letter-spacing:5px;text-transform:uppercase;color:var(--g);text-align:center;margin-bottom:18px}
.blog-s .blog-title{font-family:'Bodoni Moda',serif;font-size:clamp(34px,5vw,64px);line-height:1.05;color:var(--wh);text-align:center;font-weight:700;margin-bottom:26px}
.blog-s .blog-title i{color:var(--gl);font-weight:400}
.blog-s .blog-lead{max-width:760px;margin:0 auto 56px;text-align:center;font-size:17px;line-height:1.8;color:var(--md)}
.blog-s .blog-reg{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;max-width:1200px;margin:0 auto 48px}
.blog-s .rg{border:1px solid var(--br);border-radius:4px;padding:30px 26px;background:rgba(196,163,90,.04);transition:border-color .4s,transform .4s}
.blog-s .rg:hover{border-color:var(--g);transform:translateY(-4px)}
.blog-s .rg-flag{font-size:30px;margin-bottom:14px}
.blog-s .rg-h{font-family:'Bodoni Moda',serif;font-size:22px;color:var(--wh);margin-bottom:10px}
.blog-s .rg-p{font-size:14px;line-height:1.7;color:var(--md)}
.blog-s .blog-tr{display:flex;flex-wrap:wrap;justify-content:center;gap:14px 40px;max-width:1000px;margin:0 auto 48px}
.blog-s .tr-i{display:flex;align-items:center;gap:10px;font-size:14px;color:var(--cr)}
.blog-s .tr-i span.tk{color:var(--g);font-size:16px}
.blog-s .blog-cta{text-align:center}
.blog-s .blog-cta a{display:inline-flex;align-items:center;gap:10px;background:var(--g);color:var(--bl);padding:16px 40px;border-radius:2px;font-size:14px;letter-spacing:2px;text-transform:uppercase;text-decoration:none;transition:background .3s,transform .3s}
.blog-s .blog-cta a:hover{background:var(--gl);transform:translateY(-2px)}
@media(max-width:860px){.blog-s{padding:70px 22px}.blog-s .blog-reg{grid-template-columns:1fr;gap:16px}.blog-s .blog-tr{flex-direction:column;align-items:center;gap:14px}}
</style>
<section class="blog-s reveal">
  <div class="blog-eye" data-tr>BIMOR Lojistik</div><div class="blog-eye" data-en>BIMOR Logistics</div><div class="blog-eye" data-ar>الخدمات اللوجستية</div><div class="blog-eye" data-de>BIMOR Logistik</div>
  <h2 class="blog-title" data-tr>Kendi Filomuzla<br><i>Global Teslimat</i></h2>
  <h2 class="blog-title" data-en>Global Delivery<br><i>With Our Own Fleet</i></h2>
  <h2 class="blog-title" data-ar>توصيل عالمي<br><i>بأسطولنا الخاص</i></h2>
  <h2 class="blog-title" data-de>Globale Lieferung<br><i>mit eigener Flotte</i></h2>
  <p class="blog-lead" data-tr>Biz yalnizca uretici degiliz - kendi lojistik ve nakliye sirketimiz var. Atolyeden kapiniza, araci olmadan, tek elden teslim ediyoruz. Bu rotalarda zaten her gun calisiyoruz; urununuz guvenli ellerde.</p>
  <p class="blog-lead" data-en>We're not just a manufacturer - we run our own logistics and transport company. From our workshop to your door, no middleman, all handled in-house. We already operate these routes every day; your order is in safe hands.</p>
  <p class="blog-lead" data-ar>لسنا مجرد مصنّع - لدينا شركة النقل واللوجستيات الخاصة بنا. من ورشتنا إلى بابك، دون وسطاء، بإدارة كاملة منّا. نعمل على هذه الطرق يومياً؛ طلبك في أيدٍ أمينة.</p>
  <p class="blog-lead" data-de>Wir sind nicht nur Hersteller - wir betreiben unsere eigene Logistik- und Transportfirma. Von unserer Werkstatt bis zu Ihrer Tur, ohne Zwischenhandler, alles aus einer Hand. Wir befahren diese Routen taglich; Ihre Bestellung ist in sicheren Handen.</p>
  <div class="blog-reg">
    <div class="rg">
      <div class="rg-flag">&#127466;&#127482;</div>
      <div class="rg-h" data-tr>Tum Avrupa</div><div class="rg-h" data-en>All of Europe</div><div class="rg-h" data-ar>كل أوروبا</div><div class="rg-h" data-de>Ganz Europa</div>
      <p class="rg-p" data-tr>Bulgaristan, Romanya, Yunanistan, Karadag ve Avrupa'nin her noktasina duzenli sefer.</p>
      <p class="rg-p" data-en>Regular routes to Bulgaria, Romania, Greece, Montenegro and everywhere across Europe.</p>
      <p class="rg-p" data-ar>رحلات منتظمة إلى بلغاريا ورومانيا واليونان والجبل الأسود وكل أنحاء أوروبا.</p>
      <p class="rg-p" data-de>Regelmassige Fahrten nach Bulgarien, Rumanien, Griechenland, Montenegro und in ganz Europa.</p>
    </div>
    <div class="rg">
      <div class="rg-flag">&#128717;</div>
      <div class="rg-h" data-tr>Orta Dogu</div><div class="rg-h" data-en>Middle East</div><div class="rg-h" data-ar>الشرق الأوسط</div><div class="rg-h" data-de>Naher Osten</div>
      <p class="rg-p" data-tr>Karadan Iran hatti ve Orta Dogu'ya aktif tasimacilik - Suudi Arabistan, BAE, Katar ve daha fazlasi.</p>
      <p class="rg-p" data-en>Active overland Iran route and delivery across the Middle East - Saudi Arabia, UAE, Qatar and more.</p>
      <p class="rg-p" data-ar>خط بري نشط إلى إيران وتوصيل إلى الشرق الأوسط - السعودية والإمارات وقطر والمزيد.</p>
      <p class="rg-p" data-de>Aktive Landroute in den Iran und Lieferung in den Nahen Osten - Saudi-Arabien, VAE, Katar und mehr.</p>
    </div>
    <div class="rg">
      <div class="rg-flag">&#127479;&#127482;</div>
      <div class="rg-h" data-tr>Rusya & BDT</div><div class="rg-h" data-en>Russia & CIS</div><div class="rg-h" data-ar>روسيا ورابطة الدول</div><div class="rg-h" data-de>Russland & GUS</div>
      <p class="rg-p" data-tr>Moskova hatti aktif. Cogu ureticinin giremedigi pazara kendi araclarimizla dogrudan teslimat.</p>
      <p class="rg-p" data-en>Moscow route active. Direct delivery with our own vehicles to a market most makers can't reach.</p>
      <p class="rg-p" data-ar>خط موسكو نشط. توصيل مباشر بمركباتنا إلى سوق يصعب على معظم المصنّعين الوصول إليه.</p>
      <p class="rg-p" data-de>Moskau-Route aktiv. Direktlieferung mit eigenen Fahrzeugen in einen Markt, den die meisten kaum erreichen.</p>
    </div>
  </div>
  <div class="blog-tr">
    <div class="tr-i"><span class="tk">&#10022;</span><span data-tr>Kendi filomuz - aracisiz</span><span data-en>Our own fleet - no middleman</span><span data-ar>أسطولنا الخاص - بلا وسطاء</span><span data-de>Eigene Flotte - kein Zwischenhandler</span></div>
    <div class="tr-i"><span class="tk">&#10022;</span><span data-tr>Sigortali & guvenli tasima</span><span data-en>Insured & safe transport</span><span data-ar>نقل مؤمّن وآمن</span><span data-de>Versicherter & sicherer Transport</span></div>
    <div class="tr-i"><span class="tk">&#10022;</span><span data-tr>Zamaninda teslimat</span><span data-en>On-time delivery</span><span data-ar>تسليم في الوقت المحدد</span><span data-de>Punktliche Lieferung</span></div>
    <div class="tr-i"><span class="tk">&#10022;</span><span data-tr>Ureticiden kapiya</span><span data-en>Factory to your door</span><span data-ar>من المصنع إلى بابك</span><span data-de>Vom Werk bis zur Tur</span></div>
  </div>
  <div class="blog-cta">
    <a href="https://wa.me/905446452430?text=Merhaba%20BIMOR%2C%20teslimat%20ve%20lojistik%20hakk%C4%B1nda%20bilgi%20almak%20istiyorum." target="_blank"><span>&#128172;</span><span data-tr>Teslimat icin fiyat alin</span><span data-en>Get a delivery quote</span><span data-ar>احصل على عرض سعر للتوصيل</span><span data-de>Lieferangebot anfragen</span></a>
  </div>
</section>
'''

def process(path):
    slug=os.path.basename(path)[:-5]
    src=open(path,encoding='utf-8').read(); changed=False
    # HEAD
    if 'og:image' not in src:
        title=re.search(r'<title>(.*?)</title>',src,re.S).group(1).strip()
        desc=re.search(r'<meta name="description" content="(.*?)">',src,re.S).group(1).strip()
        src=src.replace('</title>','</title>\n'+head_block(slug,title,desc),1); changed=True
    # de/ru CSS
    if '/*i18n-de-ru*/' not in src:
        i=src.find('</style>'); src=src[:i]+CSSINJECT+src[i:]; changed=True
    # FOOTER
    if 'bamir-ft' not in src:
        if slug=='index':
            src=re.sub(r'<footer>.*?</footer>',FOOTER,src,count=1,flags=re.S)
        elif '<!-- FLOATING WHATSAPP -->' in src:
            src=src.replace('<!-- FLOATING WHATSAPP -->',FOOTER+'\n\n<!-- FLOATING WHATSAPP -->',1)
        else:
            i=src.rfind('<script>'); src=src[:i]+FOOTER+'\n\n'+src[i:]
        changed=True
    # LOGISTICS (index only)
    if slug=='index' and 'blog-s' not in src:
        if '<!-- CONTACT -->' in src: src=src.replace('<!-- CONTACT -->',LOGI+'<!-- CONTACT -->',1)
        else: src=re.sub(r'(<footer class="bamir-ft">)',LOGI+r'\1',src,count=1)
        changed=True
    if changed: open(path,'w',encoding='utf-8').write(src)
    print(('degisti ' if changed else 'atlandi ')+slug)

if __name__=='__main__':
    if not os.path.exists('index.html'):
        print('HATA: repo kokunde calistir (index.html bulunamadi)'); sys.exit(1)
    build_og()
    for f in sorted(glob.glob('*.html')): process(f)
    print('PR1 TAMAM')
