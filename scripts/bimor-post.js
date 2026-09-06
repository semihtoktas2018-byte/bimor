const fetch = require('node-fetch');

// ─── REKLAM METİNLERİ ───────────────────────────────────────────────
const posts = [
  {
    tr: `✨ BIMOR Luxury Furniture\n\nEl işçiliği ve altın varak — her parça bir sanat eseri.\n📦 Türkiye geneli teslimat\n🌍 30+ ülkeye ihracat\n💬 WhatsApp: +90 544 645 24 30\n🔗 bimor.store`,
    en: `✨ BIMOR Luxury Furniture\n\nHandcrafted gold leaf furniture — every piece is art.\n📦 Turkey-wide delivery\n🌍 Export to 30+ countries\n💬 WhatsApp: +90 544 645 24 30\n🔗 bimor.store`,
    de: `✨ BIMOR Luxury Furniture\n\nHandgefertigte Möbel mit Blattgold — jedes Stück ein Kunstwerk.\n📦 Lieferung in der gesamten Türkei\n🌍 Export in 30+ Länder\n💬 WhatsApp: +90 544 645 24 30\n🔗 bimor.store`,
    ar: `✨ BIMOR للأثاث الفاخر\n\nأثاث يدوي بورق الذهب — كل قطعة تحفة فنية.\n📦 توصيل في جميع أنحاء تركيا\n🌍 تصدير لأكثر من 30 دولة\n💬 واتساب: 905446452430+\n🔗 bimor.store`
  },
  {
    tr: `🛋️ Bağdat Koleksiyonu — BIMOR\n\nBaşkentin ihtişamını evinize taşıyın.\nVelvet kumaş · Altın oymalı çerçeve · Özel sipariş\n\n📞 +90 544 645 24 30\n🌐 bimor.store`,
    en: `🛋️ Bağdat Collection — BIMOR\n\nBring the grandeur of the capital to your home.\nVelvet fabric · Gold carved frame · Custom order\n\n📞 +90 544 645 24 30\n🌐 bimor.store`,
    de: `🛋️ Bağdat Kollektion — BIMOR\n\nBringen Sie den Glanz der Hauptstadt in Ihr Zuhause.\nSamtstoff · Goldgeschnitzter Rahmen · Auf Bestellung\n\n📞 +90 544 645 24 30\n🌐 bimor.store`,
    ar: `🛋️ مجموعة بغداد — BIMOR\n\nأحضروا بهاء العاصمة إلى منزلكم.\nقماش مخملي · إطار منحوت بالذهب · حسب الطلب\n\n📞 905446452430+\n🌐 bimor.store`
  },
  {
    tr: `🏆 Fabrikadan Direkt — BIMOR\n\nAracı yok. Fabrika fiyatına Avrupa kalitesi.\n✅ Özel üretim\n✅ Toptan & perakende\n✅ İnegöl, Bursa\n\nTeklif için: wa.me/905446452430`,
    en: `🏆 Direct from Factory — BIMOR\n\nNo middlemen. European quality at factory price.\n✅ Custom production\n✅ Wholesale & retail\n✅ İnegöl, Bursa · Turkey\n\nGet a quote: wa.me/905446452430`,
    de: `🏆 Direkt vom Hersteller — BIMOR\n\nKeine Zwischenhändler. Europäische Qualität zum Fabrikpreis.\n✅ Individuelle Fertigung\n✅ Groß- & Einzelhandel\n✅ İnegöl, Bursa · Türkei\n\nAngebot: wa.me/905446452430`,
    ar: `🏆 مباشرة من المصنع — BIMOR\n\nلا وسطاء. جودة أوروبية بسعر المصنع.\n✅ تصنيع مخصص\n✅ جملة وتجزئة\n✅ إينيغول، بورصة · تركيا\n\nاحصل على عرض: wa.me/905446452430`
  },
  {
    tr: `🌟 Luxury Furniture Export — BIMOR\n\nTürkiye'nin mobilya kalbi İnegöl'den dünyaya.\n\n🪑 Koltuk takımları\n🛋️ Özel berjerler\n🍽️ Yemek odası grupları\n\n📱 WhatsApp: +90 544 645 24 30\n💻 bimor.store`,
    en: `🌟 Luxury Furniture Export — BIMOR\n\nFrom İnegöl — Turkey's furniture heart — to the world.\n\n🪑 Sofa sets\n🛋️ Custom armchairs\n🍽️ Dining room sets\n\n📱 WhatsApp: +90 544 645 24 30\n💻 bimor.store`,
    de: `🌟 Luxusmöbel Export — BIMOR\n\nVon İnegöl — dem Möbelherz der Türkei — in die Welt.\n\n🪑 Sofagarnituren\n🛋️ Maßgefertigte Sessel\n🍽️ Esszimmergruppen\n\n📱 WhatsApp: +90 544 645 24 30\n💻 bimor.store`,
    ar: `🌟 تصدير أثاث فاخر — BIMOR\n\nمن إينيغول — قلب الأثاث التركي — إلى العالم.\n\n🪑 طقم أريكة\n🛋️ مقاعد مخصصة\n🍽️ طاقم غرفة الطعام\n\n📱 واتساب: 905446452430+\n💻 bimor.store`
  },
  {
    tr: `💎 Altın Varak İşçiliği — BIMOR\n\nHer detay bir ustalık eseri.\nGerçek altın varak · El oyması ahşap · Premium velvet\n\nSizi aramak ister misiniz? Numaranızı bırakın.\n📞 +90 544 645 24 30`,
    en: `💎 Gold Leaf Craftsmanship — BIMOR\n\nEvery detail, a masterpiece of artistry.\nReal gold leaf · Hand-carved wood · Premium velvet\n\nWant us to call you? Leave your number.\n📞 +90 544 645 24 30`,
    de: `💎 Blattgold-Handwerk — BIMOR\n\nJedes Detail ein Meisterwerk.\nEchtes Blattgold · Handgeschnitztes Holz · Premium-Samt\n\nSollen wir Sie anrufen? Hinterlassen Sie Ihre Nummer.\n📞 +90 544 645 24 30`,
    ar: `💎 حرفة ورق الذهب — BIMOR\n\nكل تفصيل تحفة فنية.\nورق ذهب حقيقي · خشب منحوت يدوياً · مخمل فاخر\n\nتريدون أن نتصل بكم؟ اتركوا رقمكم.\n📞 905446452430+`
  },
  {
    tr: `🏠 Otel & Villa Projeleri — BIMOR\n\nToplu sipariş için özel fiyat.\n🏨 Otel lobisi\n🏡 Villa döşemesi\n🏢 Ofis & lounge\n\nProjeniz için teklif alın:\nwa.me/905446452430`,
    en: `🏠 Hotel & Villa Projects — BIMOR\n\nSpecial pricing for bulk orders.\n🏨 Hotel lobby\n🏡 Villa furnishing\n🏢 Office & lounge\n\nGet a quote for your project:\nwa.me/905446452430`,
    de: `🏠 Hotel & Villa Projekte — BIMOR\n\nSonderpreise für Großbestellungen.\n🏨 Hotellobby\n🏡 Villaausstattung\n🏢 Büro & Lounge\n\nAngebot für Ihr Projekt:\nwa.me/905446452430`,
    ar: `🏠 مشاريع الفنادق والفيلات — BIMOR\n\nأسعار خاصة للطلبات الكبيرة.\n🏨 لوبي الفندق\n🏡 تأثيث الفيلا\n🏢 المكتب والصالة\n\nاحصل على عرض لمشروعك:\nwa.me/905446452430`
  },
  {
    tr: `🌍 Almanya · Hollanda · Belçika — BIMOR\n\nAvrupa'ya kapıdan teslim lüks mobilya.\nDDP · Sigortalı · Profesyonel ambalaj\n\n🇩🇪🇳🇱🇧🇪 Şimdi iletişime geçin:\n+90 544 645 24 30`,
    en: `🌍 Germany · Netherlands · Belgium — BIMOR\n\nDoor-to-door luxury furniture delivery to Europe.\nDDP · Insured · Professional packaging\n\n🇩🇪🇳🇱🇧🇪 Contact us now:\n+90 544 645 24 30`,
    de: `🌍 Deutschland · Niederlande · Belgien — BIMOR\n\nLuxusmöbel-Lieferung direkt an Ihre Tür.\nDDP · Versichert · Professionelle Verpackung\n\n🇩🇪🇳🇱🇧🇪 Jetzt Kontakt aufnehmen:\n+90 544 645 24 30`,
    ar: `🌍 ألمانيا · هولندا · بلجيكا — BIMOR\n\nتوصيل أثاث فاخر من الباب للباب إلى أوروبا.\nDDP · مؤمّن · تغليف احترافي\n\n🇩🇪🇳🇱🇧🇪 تواصل الآن:\n905446452430+`
  },
  {
    tr: `🕌 Orta Doğu & Körfez — BIMOR\n\nBAE · Suudi Arabistan · Katar · Kuveyt\nLüks mobilyada Türk kalitesi.\n\n🤍 Özel koleksiyon mevcut\n📦 Kapıdan teslim\n\nWhatsApp: wa.me/905446452430`,
    en: `🕌 Middle East & Gulf — BIMOR\n\nUAE · Saudi Arabia · Qatar · Kuwait\nTurkish quality in luxury furniture.\n\n🤍 Exclusive collections available\n📦 Door-to-door delivery\n\nWhatsApp: wa.me/905446452430`,
    de: `🕌 Naher Osten & Golf — BIMOR\n\nVAE · Saudi-Arabien · Katar · Kuwait\nTürkische Qualität in Luxusmöbeln.\n\n🤍 Exklusive Kollektionen verfügbar\n📦 Türzustellung\n\nWhatsApp: wa.me/905446452430`,
    ar: `🕌 الشرق الأوسط والخليج — BIMOR\n\nالإمارات · السعودية · قطر · الكويت\nجودة تركية في الأثاث الفاخر.\n\n🤍 مجموعات حصرية متاحة\n📦 توصيل من الباب للباب\n\nواتساب: wa.me/905446452430`
  }
];

// ─── HELPERS ────────────────────────────────────────────────────────
function pickPost() {
  const hour = new Date().getUTCHours();
  // Dile göre saat bazlı seçim: sabah TR, öğlen EN, ikindi DE, akşam AR
  const langMap = { 6: 'tr', 10: 'en', 14: 'de', 18: 'ar', 22: 'tr' };
  const lang = langMap[hour] || 'en';
  const idx = Math.floor(Date.now() / 3600000) % posts.length;
  return { text: posts[idx][lang], lang };
}

async function postFacebook(text) {
  const { FB_PAGE_ID, FB_PAGE_TOKEN } = process.env;
  if (!FB_PAGE_ID || !FB_PAGE_TOKEN) { console.log('⚠️  FB secret yok, atlandı'); return; }
  const res = await fetch(`https://graph.facebook.com/v19.0/${FB_PAGE_ID}/feed`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text, access_token: FB_PAGE_TOKEN })
  });
  const data = await res.json();
  if (data.id) console.log(`✅ Facebook: ${data.id}`);
  else console.log('❌ Facebook hatası:', JSON.stringify(data));
}

async function postInstagram(text) {
  const { IG_BUSINESS_ID, FB_PAGE_TOKEN } = process.env;
  if (!IG_BUSINESS_ID || !FB_PAGE_TOKEN) { console.log('⚠️  IG secret yok, atlandı'); return; }
  // IG sadece görsel ile çalışır — metin içeren yorum olarak ekle
  // Görsel yoksa bu adım atlanır; görseller eklenince aktifleşir
  console.log('ℹ️  Instagram: Görsel gerektirir. scripts/gorseller/ klasörüne ürün fotoğrafı eklendiğinde aktif olur.');
}

async function postTelegram(text) {
  const { TG_BOT_TOKEN, TG_CHANNEL } = process.env;
  if (!TG_BOT_TOKEN || !TG_CHANNEL) { console.log('⚠️  Telegram secret yok, atlandı'); return; }
  const res = await fetch(`https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: TG_CHANNEL, text, parse_mode: 'HTML' })
  });
  const data = await res.json();
  if (data.ok) console.log(`✅ Telegram: ${data.result.message_id}`);
  else console.log('❌ Telegram hatası:', JSON.stringify(data));
}

// ─── MAIN ────────────────────────────────────────────────────────────
async function main() {
  const { text, lang } = pickPost();
  console.log(`\n📢 BIMOR Otomatik Paylaşım — ${new Date().toISOString()}`);
  console.log(`🌐 Dil: ${lang.toUpperCase()}\n`);
  console.log('Metin:', text.substring(0, 80) + '...\n');
  await Promise.all([
    postFacebook(text),
    postInstagram(text),
    postTelegram(text)
  ]);
  console.log('\n✅ Tamamlandı.');
}

main().catch(console.error);
