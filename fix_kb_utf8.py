#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BIMOR duzeltme: (1) footer + lojistik bolumundeki bozuk Turkce/Almanca karakterleri
# duzeltir, (2) "BIMOR Lojistik" -> KB Logistics (bir Bulak Trans istiraki).
# Repo kokunde: python3 fix_kb_utf8.py   (idempotent — tekrar calistirilabilir)
import re, os, sys

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
      <p class="bf-tag" data-tr>İnegöl'den dünyaya — özel üretim, toptan satış ve ihracat. Avrupa, Orta Doğu ve Rusya'ya güvenli teslimat.</p>
      <p class="bf-tag" data-en>From İnegöl to the world — custom production, wholesale &amp; export. Safe delivery to Europe, the Middle East and Russia.</p>
      <p class="bf-tag" data-ar>من إينيغول إلى العالم — إنتاج مخصص وبيع بالجملة وتصدير. توصيل آمن إلى أوروبا والشرق الأوسط وروسيا.</p>
      <p class="bf-tag" data-de>Von İnegöl in die Welt — Maßfertigung, Großhandel &amp; Export. Sichere Lieferung nach Europa, in den Nahen Osten und nach Russland.</p>
      <div class="bf-soc">
        <a href="https://wa.me/905446452430" target="_blank" aria-label="WhatsApp">&#128172;</a>
        <a href="https://instagram.com/bimor_store" target="_blank" aria-label="Instagram">&#128247;</a>
        <a href="https://facebook.com/profile.php?id=61575530913797" target="_blank" aria-label="Facebook">&#128100;</a>
      </div>
    </div>
    <div>
      <h5 data-tr>Adreslerimiz</h5><h5 data-en>Our Locations</h5><h5 data-ar>عناويننا</h5><h5 data-de>Unsere Standorte</h5>
      <div class="bf-adr">
        <strong data-tr>Tasarım &amp; Üretim Merkezi</strong><strong data-en>Design &amp; Production Center</strong><strong data-ar>مركز التصميم والإنتاج</strong><strong data-de>Design- &amp; Produktionszentrum</strong>
        Yenice Mah., İnegöl / Bursa
      </div>
      <div class="bf-adr">
        <strong data-tr>Merkez Ofis &amp; Lojistik</strong><strong data-en>Head Office &amp; Logistics</strong><strong data-ar>المكتب الرئيسي واللوجستيات</strong><strong data-de>Hauptbüro &amp; Logistik</strong>
        Bursa Gıda Toptancıları Sitesi, Nilüfer / Bursa
      </div>
    </div>
    <div>
      <h5 data-tr>Teslimat Bölgeleri</h5><h5 data-en>Delivery Regions</h5><h5 data-ar>مناطق التوصيل</h5><h5 data-de>Lieferregionen</h5>
      <div class="bf-reg" data-tr><strong>Avrupa:</strong> Bulgaristan &middot; Romanya &middot; Yunanistan &middot; Karadağ<br><strong>Orta Doğu:</strong> S. Arabistan &middot; BAE &middot; Katar &middot; Kuveyt &middot; Ürdün &middot; İran<br><strong>Rusya:</strong> Moskova &amp; Rusya geneli</div>
      <div class="bf-reg" data-en><strong>Europe:</strong> Bulgaria &middot; Romania &middot; Greece &middot; Montenegro<br><strong>Middle East:</strong> Saudi Arabia &middot; UAE &middot; Qatar &middot; Kuwait &middot; Jordan &middot; Iran<br><strong>Russia:</strong> Moscow &amp; across Russia</div>
      <div class="bf-reg" data-ar dir="rtl"><strong>أوروبا:</strong> بلغاريا &middot; رومانيا &middot; اليونان &middot; الجبل الأسود<br><strong>الشرق الأوسط:</strong> السعودية &middot; الإمارات &middot; قطر &middot; الكويت &middot; الأردن &middot; إيران<br><strong>روسيا:</strong> موسكو وجميع أنحاء روسيا</div>
      <div class="bf-reg" data-de><strong>Europa:</strong> Bulgarien &middot; Rumänien &middot; Griechenland &middot; Montenegro<br><strong>Naher Osten:</strong> Saudi-Arabien &middot; VAE &middot; Katar &middot; Kuwait &middot; Jordanien &middot; Iran<br><strong>Russland:</strong> Moskau &amp; russlandweit</div>
    </div>
    <div>
      <h5 data-tr>İletişim</h5><h5 data-en>Contact</h5><h5 data-ar>تواصل</h5><h5 data-de>Kontakt</h5>
      <ul>
        <li><a href="https://wa.me/905446452430" target="_blank">+90 544 645 24 30</a></li>
        <li><a href="https://instagram.com/bimor_store" target="_blank">@bimor_store</a></li>
        <li><a href="https://facebook.com/profile.php?id=61575530913797" target="_blank">Facebook</a></li>
        <li><a href="https://bimor.store">bimor.store</a></li>
      </ul>
    </div>
  </div>
  <div class="bf-bot">
    <span>&copy; 2026 BIMOR Luxury Furniture. <span data-tr>Tüm hakları saklıdır.</span><span data-en>All rights reserved.</span><span data-ar>جميع الحقوق محفوظة.</span><span data-de>Alle Rechte vorbehalten.</span></span>
    <span class="bf-sig">A <b>BAMIR ONLINE STORE'S</b> PRODUCTION</span>
  </div>
</footer>'''

LOGI = r'''<!-- LOGISTICS ADVANTAGE -->
<style>
.blog-s{background:var(--bl);color:var(--cr);padding:110px 80px;position:relative;z-index:2;overflow:hidden}
.blog-s .blog-eye{font-size:12px;letter-spacing:5px;text-transform:uppercase;color:var(--g);text-align:center;margin-bottom:18px}
.blog-s .blog-title{font-family:'Bodoni Moda',serif;font-size:clamp(34px,5vw,64px);line-height:1.05;color:var(--wh);text-align:center;font-weight:700;margin-bottom:16px}
.blog-s .blog-title i{color:var(--gl);font-weight:400}
.blog-s .blog-aff{text-align:center;font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--gl);margin:0 auto 34px}
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
  <div class="blog-eye" data-tr>KB Logistics</div><div class="blog-eye" data-en>KB Logistics</div><div class="blog-eye" data-ar>KB Logistics</div><div class="blog-eye" data-de>KB Logistics</div>
  <h2 class="blog-title" data-tr>Kendi Filomuzla<br><i>Global Teslimat</i></h2>
  <h2 class="blog-title" data-en>Global Delivery<br><i>With Our Own Fleet</i></h2>
  <h2 class="blog-title" data-ar>توصيل عالمي<br><i>بأسطولنا الخاص</i></h2>
  <h2 class="blog-title" data-de>Globale Lieferung<br><i>mit eigener Flotte</i></h2>
  <div class="blog-aff" data-tr>Lojistik firmamız KB Logistics — bir Bulak Trans iştirakidir</div>
  <div class="blog-aff" data-en>Our logistics company KB Logistics — a Bulak Trans affiliate</div>
  <div class="blog-aff" data-ar>شركتنا اللوجستية KB Logistics — إحدى شركات Bulak Trans</div>
  <div class="blog-aff" data-de>Unsere Logistikfirma KB Logistics — ein Bulak-Trans-Beteiligungsunternehmen</div>
  <p class="blog-lead" data-tr>Biz yalnızca üretici değiliz — lojistik firmamız KB Logistics ile atölyeden kapınıza, aracı olmadan, tek elden teslim ediyoruz. Bu rotalarda zaten her gün çalışıyoruz; ürününüz güvenli ellerde.</p>
  <p class="blog-lead" data-en>We're not just a manufacturer — with KB Logistics, our own fleet, we deliver from our workshop to your door, no middleman, all in-house. We already run these routes every day; your order is in safe hands.</p>
  <p class="blog-lead" data-ar>لسنا مجرد مصنّع — نوصّل عبر KB Logistics، أسطولنا الخاص، من ورشتنا إلى بابك دون وسطاء وبإدارة كاملة منّا. نعمل على هذه الطرق يومياً؛ طلبك في أيدٍ أمينة.</p>
  <p class="blog-lead" data-de>Wir sind nicht nur Hersteller — mit KB Logistics, unserer eigenen Flotte, liefern wir von der Werkstatt bis zu Ihrer Tür, ohne Zwischenhändler, alles aus einer Hand. Wir befahren diese Routen täglich; Ihre Bestellung ist in sicheren Händen.</p>
  <div class="blog-reg">
    <div class="rg">
      <div class="rg-flag">&#127466;&#127482;</div>
      <div class="rg-h" data-tr>Tüm Avrupa</div><div class="rg-h" data-en>All of Europe</div><div class="rg-h" data-ar>كل أوروبا</div><div class="rg-h" data-de>Ganz Europa</div>
      <p class="rg-p" data-tr>Bulgaristan, Romanya, Yunanistan, Karadağ ve Avrupa'nın her noktasına düzenli sefer.</p>
      <p class="rg-p" data-en>Regular routes to Bulgaria, Romania, Greece, Montenegro and everywhere across Europe.</p>
      <p class="rg-p" data-ar>رحلات منتظمة إلى بلغاريا ورومانيا واليونان والجبل الأسود وكل أنحاء أوروبا.</p>
      <p class="rg-p" data-de>Regelmäßige Fahrten nach Bulgarien, Rumänien, Griechenland, Montenegro und in ganz Europa.</p>
    </div>
    <div class="rg">
      <div class="rg-flag">&#128717;</div>
      <div class="rg-h" data-tr>Orta Doğu</div><div class="rg-h" data-en>Middle East</div><div class="rg-h" data-ar>الشرق الأوسط</div><div class="rg-h" data-de>Naher Osten</div>
      <p class="rg-p" data-tr>Karadan İran hattı ve Orta Doğu'ya aktif taşımacılık — Suudi Arabistan, BAE, Katar ve daha fazlası.</p>
      <p class="rg-p" data-en>Active overland Iran route and delivery across the Middle East — Saudi Arabia, UAE, Qatar and more.</p>
      <p class="rg-p" data-ar>خط بري نشط إلى إيران وتوصيل إلى الشرق الأوسط — السعودية والإمارات وقطر والمزيد.</p>
      <p class="rg-p" data-de>Aktive Landroute in den Iran und Lieferung in den Nahen Osten — Saudi-Arabien, VAE, Katar und mehr.</p>
    </div>
    <div class="rg">
      <div class="rg-flag">&#127479;&#127482;</div>
      <div class="rg-h" data-tr>Rusya &amp; BDT</div><div class="rg-h" data-en>Russia &amp; CIS</div><div class="rg-h" data-ar>روسيا ورابطة الدول</div><div class="rg-h" data-de>Russland &amp; GUS</div>
      <p class="rg-p" data-tr>Moskova hattı aktif. Çoğu üreticinin giremediği pazara kendi araçlarımızla doğrudan teslimat.</p>
      <p class="rg-p" data-en>Moscow route active. Direct delivery with our own vehicles to a market most makers can't reach.</p>
      <p class="rg-p" data-ar>خط موسكو نشط. توصيل مباشر بمركباتنا إلى سوق يصعب على معظم المصنّعين الوصول إليه.</p>
      <p class="rg-p" data-de>Moskau-Route aktiv. Direktlieferung mit eigenen Fahrzeugen in einen Markt, den die meisten kaum erreichen.</p>
    </div>
  </div>
  <div class="blog-tr">
    <div class="tr-i"><span class="tk">&#10022;</span><span data-tr>Kendi filomuz — aracısız</span><span data-en>Our own fleet — no middleman</span><span data-ar>أسطولنا الخاص — بلا وسطاء</span><span data-de>Eigene Flotte — kein Zwischenhändler</span></div>
    <div class="tr-i"><span class="tk">&#10022;</span><span data-tr>Sigortalı &amp; güvenli taşıma</span><span data-en>Insured &amp; safe transport</span><span data-ar>نقل مؤمّن وآمن</span><span data-de>Versicherter &amp; sicherer Transport</span></div>
    <div class="tr-i"><span class="tk">&#10022;</span><span data-tr>Zamanında teslimat</span><span data-en>On-time delivery</span><span data-ar>تسليم في الوقت المحدد</span><span data-de>Pünktliche Lieferung</span></div>
    <div class="tr-i"><span class="tk">&#10022;</span><span data-tr>Üreticiden kapıya</span><span data-en>Factory to your door</span><span data-ar>من المصنع إلى بابك</span><span data-de>Vom Werk bis zur Tür</span></div>
  </div>
  <div class="blog-cta">
    <a href="https://wa.me/905446452430?text=Merhaba%20BIMOR%2C%20teslimat%20ve%20lojistik%20hakk%C4%B1nda%20bilgi%20almak%20istiyorum." target="_blank"><span>&#128172;</span><span data-tr>Teslimat için fiyat alın</span><span data-en>Get a delivery quote</span><span data-ar>احصل على عرض سعر للتوصيل</span><span data-de>Lieferangebot anfragen</span></a>
  </div>
</section>
'''

def main():
    if not os.path.exists('index.html'):
        print('HATA: repo kokunde calistir'); sys.exit(1)
    src = open('index.html', encoding='utf-8').read()
    # 1) footer bloğunu (style + footer) düzgün UTF-8 sürümle değiştir
    src2 = re.sub(r'<style>\s*\.bamir-ft\{.*?</footer>', FOOTER, src, count=1, flags=re.S)
    # 2) lojistik bölümünü KB Logistics sürümüyle değiştir
    src2 = re.sub(r'<!-- LOGISTICS ADVANTAGE -->.*?</section>', LOGI.strip(), src2, count=1, flags=re.S)
    if src2 == src:
        print('UYARI: degisiklik yapilamadi (bloklar bulunamadi?)')
    else:
        open('index.html','w',encoding='utf-8').write(src2)
        print('index.html guncellendi (footer + KB Logistics)')

    # Diger 10 urun sayfasindaki footer'i da duzgun UTF-8 ile degistir
    import glob
    for f in glob.glob('*.html'):
        if f == 'index.html': continue
        t = open(f, encoding='utf-8').read()
        t2 = re.sub(r'<style>\s*\.bamir-ft\{.*?</footer>', FOOTER, t, count=1, flags=re.S)
        if t2 != t:
            open(f,'w',encoding='utf-8').write(t2); print('footer duzeltildi:', f)
    print('DUZELTME TAMAM')

if __name__ == '__main__':
    main()
