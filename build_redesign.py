#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BIMOR yeni tasarim rollout — urun sayfalarini yeni index.html tasarim diliyle
# yeniden kurar. Tasarim sistemi (CSS, footer, KB Logistics seridi, fontlar)
# DOGRUDAN index.html'den okunur -> birebir tutarlilik.
# Repo kokunde: python3 build_redesign.py   (idempotent)
import re, os, sys
from urllib.parse import quote

SITE = "https://bimor.store"

# ---- index.html'den tasarim sistemini cek ----
idx = open('index.html', encoding='utf-8').read()
STYLE = re.search(r'<style>(.*?)</style>', idx, re.S).group(1)
FONTS = re.search(r'(<link href="https://fonts\.googleapis\.com/css2\?family=Fraunces[^>]*/>)', idx).group(1)
FOOTER = re.search(r'(<footer>.*?</footer>)', idx, re.S).group(1)
# export / KB Logistics seridi: <div class="export" ...> ... </div> (split section'in ikinci cocugu)
EXPORT = re.search(r'(<div class="export"[^>]*>.*?)</section>', idx, re.S).group(1).rstrip()

# ---- urun-ozel ek CSS ----
ADDCSS = """
/* ===== PRODUCT PAGE ADDITIONS ===== */
.navback{font-size:13px;color:var(--muted)}.navback:hover{color:var(--plum)}
.phero{display:grid;grid-template-columns:1.1fr 1fr;min-height:82vh;align-items:center}
.phero .pimg{position:relative;height:82vh;min-height:560px}
.phero .pimg img{width:100%;height:100%;object-fit:cover}
.phero .ptext{padding:40px 56px}
.phero .ptext h1{font-family:var(--disp);font-weight:400;font-size:clamp(46px,6.4vw,92px);line-height:1;margin:16px 0 20px;letter-spacing:-.01em}
.phero .ptext h1 .pl{color:var(--plum);font-style:italic}
.phero p.pdesc{max-width:440px;font-size:16px;line-height:1.85;color:var(--muted);margin-bottom:30px}
@media(max-width:960px){.phero{grid-template-columns:1fr}.phero .pimg{height:56vh;min-height:380px}.phero .ptext{padding:40px 20px}}
.gal{padding:100px 0}
.gal h2{font-family:var(--disp);font-weight:400;font-size:clamp(30px,3.6vw,48px);margin-bottom:36px}
.gal h2 .pl{color:var(--plum);font-style:italic}
.galgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.galgrid .gi{aspect-ratio:4/5;overflow:hidden;border-radius:4px;border:1px solid var(--line)}
.galgrid .gi img{width:100%;height:100%;object-fit:cover;transition:transform .8s}
.galgrid .gi:hover img{transform:scale(1.06)}
@media(max-width:960px){.galgrid{grid-template-columns:1fr 1fr}}
.pdetail{background:var(--cream);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.pdetail .dl{display:grid;grid-template-columns:1fr 1fr;gap:56px;padding:90px 0;align-items:center}
.pdetail h2{font-family:var(--disp);font-weight:400;font-size:clamp(30px,3.6vw,48px);line-height:1.08;margin-bottom:20px}
.pdetail h2 .pl{color:var(--plum);font-style:italic}
.pdetail p.db{color:var(--muted);font-size:15px;line-height:1.9;max-width:460px}
.specs{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.spec{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:20px 22px}
.spec .sl{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:6px;font-weight:600}
.spec .sv{font-size:14px;color:var(--ink)}
@media(max-width:960px){.pdetail .dl{grid-template-columns:1fr;gap:32px;padding:56px 0}}
"""

# ---- cok dilli yardimci ----
def ml(tr, en, ar, de, ru, tag='span'):
    return (f'<{tag} data-tr>{tr}</{tag}><{tag} data-en>{en}</{tag}>'
            f'<{tag} data-ar>{ar}</{tag}><{tag} data-de>{de}</{tag}><{tag} data-ru>{ru}</{tag}>')

# ---- ortak etiketler ----
L = {
 'coll':    ('Koleksiyonu','Collection','مجموعة','Kollektion','Коллекция'),
 'gallery': ('Galeri','Gallery','المعرض','Galerie','Галерея'),
 'quote':   ('Fiyat & Katalog Al →','Get Price & Catalog →','احصل على السعر والكتالوج →','Preis & Katalog →','Цена и каталог →'),
 'navquote':('Teklif Al →','Get a Quote →','اطلب عرضاً →','Angebot →','Запросить цену →'),
 'back':    ('Tüm Koleksiyonlar','All Collections','كل المجموعات','Alle Kollektionen','Все коллекции'),
 'home':    ('Ana Sayfa','Home','الرئيسية','Start','Главная'),
 'colls':   ('Koleksiyonlar','Collections','المجموعات','Kollektionen','Коллекции'),
 'export':  ('İhracat','Export','التصدير','Export','Экспорт'),
 'contact': ('İletişim','Contact','تواصل','Kontakt','Контакты'),
 'details': ('Ürün Detayları','Product Details','تفاصيل المنتج','Produktdetails','Детали изделия'),
}
# spec etiketleri
SL = {
 'mat': ('Malzeme','Material','المادة','Material','Материал'),
 'uph': ('Döşeme','Upholstery','التنجيد','Polsterung','Обивка'),
 'mad': ('Üretim','Made In','الصنع','Herstellung','Производство'),
 'del': ('Teslimat','Delivery','التسليم','Lieferung','Доставка'),
}
# spec degerleri (ortak)
GOLD_STD = ('Masif Ahşap · Altın Varak','Solid Wood · Gold Leaf','خشب صلب · ورق الذهب','Massivholz · Blattgold','Массив дерева · Сусальное золото')
GOLD_REAL= ('Masif Ahşap · Gerçek Altın Varak','Solid Wood · Real Gold Leaf','خشب صلب · ورق ذهب حقيقي','Massivholz · Echtes Blattgold','Массив дерева · Настоящее сусальное золото')
UPH = ('Özel kumaş · Kadife · Deri','Custom fabric · Velvet · Leather','قماش مخصص · مخمل · جلد','Sonderstoff · Samt · Leder','Ткань на заказ · Бархат · Кожа')
DEL = ('Türkiye, Orta Doğu, Avrupa, ABD','Turkey, Middle East, Europe, USA','تركيا، الشرق الأوسط، أوروبا، أمريكا','Türkei, Naher Osten, Europa, USA','Турция, Ближний Восток, Европа, США')
MADE = 'İnegöl, Bursa 🇹🇷'

# ---- kategori sozlugu (5 dil) ----
CAT = {
 'sofa':  ('Koltuk Takımı','Sofa Set','طقم كنب','Sofagarnitur','Диванный гарнитур'),
 'special':('Özel Koleksiyon','Special Collection','مجموعة خاصة','Sonderkollektion','Особая коллекция'),
 'dining':('Yemek Odası','Dining Room','غرفة طعام','Esszimmer','Столовая'),
 'chaise':('Şezlong','Chaise Lounge','أريكة استرخاء','Chaiselongue','Шезлонг'),
 'rocking':('Sallanan Koltuk','Rocking Chair','كرسي هزّاز','Schaukelstuhl','Кресло-качалка'),
}

# ---- urun verileri ----
# desc: (tr, en, ar, de, ru)
PRODUCTS = {
 'alex': {'name':'Alex','cat':'sofa','mat':GOLD_STD,
   'imgs':['alex-hero.jpg','alex-sofa.jpg','alex-berjer.jpg','alex-table.jpg'],
   'desc':("Alex koleksiyonu; çağdaş zarafetin ve klasik ustalığın mükemmel birleşimi. Minimal hatlar, premium kumaşlar ve altın varak detaylarıyla modern yaşam alanlarına özel tasarlandı.",
     "Alex collection is the perfect fusion of contemporary elegance and classic mastery. Minimal lines, premium fabrics and gold leaf details — designed for modern living spaces.",
     "مجموعة أليكس هي المزيج المثالي بين الأناقة المعاصرة والإتقان الكلاسيكي. خطوط مينيمالية وأقمشة فاخرة وتفاصيل ورق الذهب.",
     "Die Alex-Kollektion ist die perfekte Verbindung von zeitgenössischer Eleganz und klassischer Meisterschaft. Minimalistische Linien, edle Stoffe und Blattgold-Details — eigens für moderne Wohnräume entworfen.",
     "Коллекция Alex — идеальное сочетание современной элегантности и классического мастерства. Минималистичные линии, премиальные ткани и детали из сусального золота, созданные специально для современных пространств.")},
 'aslan-throne': {'name':'Aslan Throne','cat':'special','mat':GOLD_REAL,
   'imgs':['aslan-throne.jpg'],
   'desc':("Aslan Throne; BIMOR'un en prestijli koleksiyonu. Taht koltuğundan ilham alan bu özel tasarım, el oymaları, gerçek altın varak ve özel kumaşlarla güç ve zarafeti tek bir parçada buluşturuyor.",
     "Aslan Throne is BIMOR's most prestigious collection. Inspired by the throne chair, this special design merges power and elegance in one piece with hand carvings, real gold leaf and custom fabrics.",
     "أسلان ثرون هي مجموعة BIMOR الأكثر مكانة. مستوحاة من كرسي العرش، تجمع هذا التصميم الخاص بين القوة والأناقة في قطعة واحدة.",
     "Aslan Throne ist BIMORs prestigeträchtigste Kollektion. Vom Thronsessel inspiriert, vereint dieses besondere Design mit Handschnitzereien, echtem Blattgold und exklusiven Stoffen Kraft und Eleganz in einem Stück.",
     "Aslan Throne — самая престижная коллекция BIMOR. Вдохновлённый троном, этот особый дизайн соединяет силу и элегантность в одном изделии благодаря ручной резьбе, настоящему сусальному золоту и эксклюзивным тканям.")},
 'bagdat': {'name':'Bağdat','cat':'sofa','mat':GOLD_STD,
   'imgs':['bagdat-hero.jpg','bagdat-sofa.jpg','bagdat-berjer.jpg','bagdat-table.jpg'],
   'desc':("Bağdat koleksiyonu; Doğu'nun zengin kültürünü modern lüksle buluşturuyor. Görkemli ahşap oyma detaylar ve altın varak işçiliğiyle evinize saray atmosferi taşıyor.",
     "Bagdat collection merges the rich culture of the East with modern luxury. Magnificent wood carving details and gold leaf craftsmanship bring a palace atmosphere to your home.",
     "مجموعة بغداد تمزج الثقافة الشرقية الغنية مع الفخامة الحديثة. تفاصيل نحت الخشب الرائعة وورق الذهب تجلب أجواء القصر إلى منزلك.",
     "Die Bağdat-Kollektion verbindet die reiche Kultur des Orients mit modernem Luxus. Prächtige Holzschnitzereien und Blattgold-Handwerk bringen eine Palast-Atmosphäre in Ihr Zuhause.",
     "Коллекция Bağdat соединяет богатую культуру Востока с современной роскошью. Великолепная резьба по дереву и работа с сусальным золотом привносят в ваш дом атмосферу дворца.")},
 'hanedan': {'name':'Hanedan','cat':'sofa','mat':GOLD_STD,
   'imgs':['hanedan-hero.jpg','hanedan-sofa.jpg','hanedan-berjer.jpg','hanedan-table.jpg'],
   'desc':("Hanedan koleksiyonu; asaletin ve güç sembollerinin mobilyaya yansımasıdır. Görkemli boyutlar, el oymaları ve altın varak detaylarıyla sarayları andıran oturma odaları yaratır.",
     "Hanedan collection is the reflection of nobility and power symbols in furniture. Majestic dimensions, hand carvings and gold leaf details create palace-like living rooms.",
     "مجموعة هانيدان هي انعكاس النبل ورموز القوة في الأثاث. أبعاد مهيبة ونقوش يدوية وتفاصيل ورق الذهب تخلق غرف معيشة تشبه القصور.",
     "Die Hanedan-Kollektion ist der Widerschein von Adel und Machtsymbolen im Mobiliar. Majestätische Dimensionen, Handschnitzereien und Blattgold-Details schaffen palastartige Wohnzimmer.",
     "Коллекция Hanedan — отражение благородства и символов власти в мебели. Величественные размеры, ручная резьба и детали из сусального золота создают гостиные, подобные дворцовым.")},
 'milano': {'name':'Milano','cat':'dining','mat':GOLD_STD,
   'imgs':['milano-hero.jpg','milano-sofa.jpg','milano-berjer.jpg','milano-table.jpg','milano-dining.jpg','milano-detail.jpg'],
   'desc':("Milano koleksiyonu; İtalyan tasarım ruhunu İnegöl'ün usta ellerinde yeniden yorumluyor. Zarif yemek masası, özel sandalyeler ve altın varak detaylarıyla sofranızı şölene dönüştürür.",
     "Milano collection reinterprets the Italian design spirit through İnegöl's master hands. Elegant dining table, custom chairs and gold leaf details transform your dining into a feast.",
     "مجموعة ميلانو تعيد تفسير روح التصميم الإيطالي عبر أيدي حرفيي إينيغول الماهرة. طاولة طعام أنيقة وكراسي مخصصة وتفاصيل ورق الذهب.",
     "Die Milano-Kollektion interpretiert den italienischen Designgeist in den Meisterhänden İnegöls neu. Ein eleganter Esstisch, maßgefertigte Stühle und Blattgold-Details verwandeln Ihre Tafel in ein Festmahl.",
     "Коллекция Milano заново переосмысляет дух итальянского дизайна в мастерских руках Инегёля. Элегантный обеденный стол, изготовленные на заказ стулья и детали из сусального золота превращают вашу трапезу в праздник.")},
 'sahmaran': {'name':'Şahmaran','cat':'sofa','mat':GOLD_STD,
   'imgs':['sahmaran-hero.jpg','sahmaran-sofa.jpg','sahmaran-berjer.jpg','sahmaran-table.jpg'],
   'desc':("Efsanevi güzelliğini mobilyaya taşıyan Şahmaran koleksiyonu; nefes kesen altın varak detaylar, özel renk ve kumaş seçenekleriyle her mekânı kraliyet sarayına dönüştürür.",
     "The Sahmaran collection brings legendary beauty to furniture — breathtaking gold leaf details and custom color options transform every space into a royal palace.",
     "مجموعة شهماران تجلب الجمال الأسطوري إلى الأثاث — تفاصيل ورق الذهب المذهلة وخيارات الألوان المخصصة تحوّل كل مكان إلى قصر ملكي.",
     "Die Şahmaran-Kollektion trägt ihre legendäre Schönheit ins Mobiliar — atemberaubende Blattgold-Details sowie individuelle Farb- und Stoffoptionen verwandeln jeden Raum in einen königlichen Palast.",
     "Коллекция Şahmaran переносит свою легендарную красоту в мебель — захватывающие детали из сусального золота и индивидуальный выбор цвета и ткани превращают любое пространство в королевский дворец.")},
 'sumen': {'name':'Sümen','cat':'chaise','mat':GOLD_STD,
   'imgs':['sumen-chaise.jpg'],
   'desc':("Sümen şezlongu; lüks dinlenmenin yeni tanımı. Ergonomik tasarımı, premium döşemesi ve zarif altın varak detaylarıyla yatak odanızı veya salonunuzu dönüştürür.",
     "Sumen chaise lounge is the new definition of luxury rest. Its ergonomic design, premium upholstery and elegant gold leaf details transform your bedroom or living room.",
     "شيزلونج سومن هو التعريف الجديد للراحة الفاخرة. تصميمه الهندسي وتنجيده الفاخر وتفاصيل ورق الذهب الأنيقة تحوّل غرفة نومك أو صالتك.",
     "Die Sümen-Chaiselongue ist die neue Definition von luxuriöser Ruhe. Ihr ergonomisches Design, edle Polsterung und elegante Blattgold-Details verwandeln Ihr Schlaf- oder Wohnzimmer.",
     "Шезлонг Sümen — новое определение роскошного отдыха. Его эргономичный дизайн, премиальная обивка и изящные детали из сусального золота преобразят вашу спальню или гостиную.")},
 'varna': {'name':'Varna','cat':'sofa','mat':GOLD_STD,
   'imgs':['varna-hero.jpg','varna-sofa.jpg','varna-berjer.jpg','varna-table.jpg','varna-dining.jpg','varna-relax.jpg','varna-detail.jpg'],
   'desc':("Varna koleksiyonu; Karadeniz'in zarafetini İnegöl'ün usta işçiliğiyle birleştiriyor. Masif ahşap çerçeve, el işlemeli altın varak ve özel döşeme seçenekleriyle villa ve otel projelerine özel.",
     "Varna collection combines Black Sea elegance with İnegöl's master craftsmanship. Solid wood frame, hand-applied gold leaf and custom upholstery options — ideal for villa and hotel projects.",
     "مجموعة فارنا تجمع بين أناقة البحر الأسود وحرفية إينيغول الماهرة. إطار خشب صلب وورق ذهب مطبق يدوياً — مثالية لمشاريع الفيلات والفنادق.",
     "Die Varna-Kollektion vereint die Eleganz des Schwarzen Meeres mit der Meisterhandwerkskunst İnegöls. Massivholzrahmen, von Hand aufgetragenes Blattgold und individuelle Polsteroptionen — ideal für Villen- und Hotelprojekte.",
     "Коллекция Varna объединяет элегантность Чёрного моря с мастерством ремесленников Инегёля. Каркас из массива дерева, нанесённое вручную сусальное золото и индивидуальная обивка — идеально для проектов вилл и отелей.")},
 'vezir': {'name':'Vezir','cat':'rocking','mat':GOLD_STD,
   'imgs':['vezir-rocking.jpg'],
   'desc':("Vezir sallanan koltuğu; geleneksel ahşap işçiliğinin modern konforla buluştuğu nadir bir tasarımdır. El oymaları ve altın varak detaylarıyla dinlenme anlarınızı lükse dönüştürür.",
     "Vezir rocking chair is a rare design where traditional woodworking meets modern comfort. Hand carvings and gold leaf details transform your moments of rest into luxury.",
     "كرسي الهزاز وزير تصميم نادر يجمع بين النجارة التقليدية والراحة الحديثة. النقوش اليدوية وتفاصيل ورق الذهب تحوّل لحظات راحتك إلى فخامة.",
     "Der Vezir-Schaukelstuhl ist ein seltenes Design, in dem traditionelle Holzhandwerkskunst auf modernen Komfort trifft. Handschnitzereien und Blattgold-Details verwandeln Ihre Momente der Ruhe in Luxus.",
     "Кресло-качалка Vezir — редкий дизайн, где традиционное столярное мастерство встречается с современным комфортом. Ручная резьба и детали из сусального золота превращают минуты отдыха в роскошь.")},
 'zera': {'name':'Zera','cat':'sofa','mat':GOLD_STD,
   'imgs':['zera-hero.jpg','zera-sofa.jpg','zera-berjer.jpg','zera-table.jpg'],
   'desc':("Zera koleksiyonu; saf zarafetin simgesi. İnce hatlar, yumuşak eğriler ve premium döşeme seçenekleriyle modern lüks yaşam alanları için özel tasarlandı.",
     "Zera collection is the symbol of pure elegance. Fine lines, soft curves and premium upholstery options — specially designed for modern luxury living spaces.",
     "مجموعة زيرا رمز الأناقة الخالصة. خطوط رفيعة ومنحنيات ناعمة وخيارات تنجيد فاخرة — مصممة خصيصاً لمساحات المعيشة الفاخرة الحديثة.",
     "Die Zera-Kollektion ist das Sinnbild reiner Eleganz. Feine Linien, sanfte Rundungen und edle Polsteroptionen — eigens für moderne, luxuriöse Wohnräume entworfen.",
     "Коллекция Zera — символ чистой элегантности. Тонкие линии, мягкие изгибы и премиальная обивка, созданные специально для современных роскошных пространств.")},
}

NAV = """<nav>
<div class="brand"><span class="b">BIMOR</span><span class="s">LUXURY FURNITURE</span></div>
<div class="nav-links"><a href="index.html">{home}</a><a href="index.html#col">{colls}</a><a href="index.html#export">{export}</a><a href="index.html#pre">{contact}</a></div>
<div class="nav-right"><a class="navback" href="index.html">← {back}</a><span class="langsw"><button class="active" onclick="setLang('tr')">TR</button><button onclick="setLang('en')">EN</button><button onclick="setLang('ar')">AR</button><button onclick="setLang('de')">DE</button><button onclick="setLang('ru')">RU</button></span><a class="btn plum" href="{wa}">{navquote}</a></div>
</nav>"""

SCRIPT = """<script>
function setLang(l){document.body.setAttribute('data-lang',l);document.documentElement.dir=(l==='ar')?'rtl':'ltr';document.documentElement.lang=l;
var b=document.querySelectorAll('.langsw button');['tr','en','ar','de','ru'].forEach(function(x,i){if(b[i])b[i].classList.toggle('active',x===l);});}
</script>"""

def wa_link(name):
    msg = f"Merhaba BIMOR, {name} koleksiyonu hakkında fiyat ve katalog almak istiyorum."
    return "https://wa.me/905446452430?text=" + quote(msg)

def esc(s):
    return s.replace('&','&amp;').replace('"','&quot;')

def build(slug, p):
    name = p['name']; cat = CAT[p['cat']]; desc = p['desc']; imgs = p['imgs']; hero = imgs[0]
    wa = wa_link(name)
    ogimg = f"{SITE}/{hero}"; url = f"{SITE}/{slug}.html"
    title = f"BIMOR — {name} {L['coll'][0]}"
    metadesc = esc(desc[0])
    jsonld = ('{"@context":"https://schema.org","@type":"Product","name":"BIMOR %s",'
              '"image":"%s","description":"%s","category":"%s",'
              '"brand":{"@type":"Brand","name":"BIMOR Luxury Furniture"},'
              '"url":"%s","manufacturer":{"@type":"Organization","name":"BIMOR Luxury Furniture","url":"https://bimor.store"}}'
              ) % (esc(name), ogimg, metadesc, esc(cat[0]), url)

    head = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8"/><meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<meta content="{metadesc}" name="description"/>
<link href="{url}" rel="canonical"/>
<meta content="product" property="og:type"/><meta content="BIMOR Luxury Furniture" property="og:site_name"/>
<meta content="{esc(title)}" property="og:title"/><meta content="{metadesc}" property="og:description"/>
<meta content="{ogimg}" property="og:image"/><meta content="{url}" property="og:url"/><meta content="tr_TR" property="og:locale"/>
<meta content="summary_large_image" name="twitter:card"/><meta content="{esc(title)}" name="twitter:title"/><meta content="{metadesc}" name="twitter:description"/><meta content="{ogimg}" name="twitter:image"/>
<script type="application/ld+json">{jsonld}</script>
{FONTS}
<style>{STYLE}{ADDCSS}</style>
</head>'''

    nav = NAV.format(home=ml(*L['home']), colls=ml(*L['colls']), export=ml(*L['export']),
                     contact=ml(*L['contact']), back=ml(*L['back']), navquote=ml(*L['navquote']), wa=wa)

    # HERO
    phero = f'''<header class="phero">
<div class="pimg"><img alt="{esc(name)}" src="{hero}"/></div>
<div class="ptext">
<span class="eyebrow">{ml(*cat)} · İnegöl</span>
<h1 class="serif">{esc(name)}</h1>
<p class="pdesc" data-tr>{desc[0]}</p><p class="pdesc" data-en>{desc[1]}</p><p class="pdesc" data-ar>{desc[2]}</p><p class="pdesc" data-de>{desc[3]}</p><p class="pdesc" data-ru>{desc[4]}</p>
<a class="btn gold" href="{wa}" target="_blank" rel="noopener">{ml(*L['quote'])}</a>
</div>
</header>'''

    # GALLERY
    tiles = "\n".join(f'<div class="gi"><img alt="{esc(name)}" src="{im}"/></div>' for im in imgs)
    gal = f'''<section class="gal wrap">
<h2 class="serif"><span class="pl">{esc(name)}</span> · {ml(*L['gallery'])}</h2>
<div class="galgrid">
{tiles}
</div>
</section>'''

    # DETAIL + SPECS
    def spec(lbl, val):
        return f'<div class="spec"><div class="sl">{ml(*lbl)}</div><div class="sv">{ml(*val)}</div></div>'
    made_spec = f'<div class="spec"><div class="sl">{ml(*SL["mad"])}</div><div class="sv">{MADE}</div></div>'
    detail = f'''<section class="pdetail"><div class="wrap"><div class="dl">
<div>
<span class="eyebrow">{ml(*L['details'])}</span>
<h2 class="serif"><span class="pl">{esc(name)}</span> {ml(*L['coll'])}</h2>
<p class="db" data-tr>{desc[0]}</p><p class="db" data-en>{desc[1]}</p><p class="db" data-ar>{desc[2]}</p><p class="db" data-de>{desc[3]}</p><p class="db" data-ru>{desc[4]}</p>
</div>
<div class="specs">
{spec(SL['mat'], p['mat'])}
{spec(SL['uph'], UPH)}
{made_spec}
{spec(SL['del'], DEL)}
</div>
</div></div></section>'''

    # KB LOGISTICS / EXPORT (index'ten birebir)
    kb = f'<section class="split">{EXPORT}</section>'

    body = f'''<body data-lang="tr">
{nav}
{phero}
{gal}
{detail}
{kb}
{FOOTER}
{SCRIPT}
</body>
</html>'''

    return head + "\n" + body

if __name__ == '__main__':
    if not os.path.exists('index.html'):
        print('HATA: repo kokunde calistir'); sys.exit(1)
    for slug, p in PRODUCTS.items():
        # tum gorseller mevcut mu kontrol
        for im in p['imgs']:
            if not os.path.exists(im):
                print(f'UYARI: {im} yok ({slug})')
        out = build(slug, p)
        open(f'{slug}.html','w',encoding='utf-8').write(out)
        print(f'yazildi: {slug}.html  ({len(p["imgs"])} gorsel)')
    print('REDESIGN TAMAM')
