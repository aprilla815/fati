# Shorts Otomasyonu

Bu depo, dikey kısa video üretimini tekrarlanabilir bir iş akışına dönüştürmek için başlangıç iskeletidir.

> Depo 28 Ekim 2026 tarihinde incelendiğinde tamamen boştu: varsayılan `master` dalında commit veya dosya, ayrıca açık issue yoktu. Bu iskelet mevcut bir uygulamayı değiştirmez; projenin ilk uygulanabilir sürümünü oluşturur.

## İlk uygulanabilir iş akışı

`examples/demo.json` içindeki başlık, sahne metinleri ve süreler kullanılarak:

1. yapılandırma doğrulanır,
2. FFmpeg için birleştirme listesi hazırlanır,
3. her sahne 1080x1920 dikey video olarak oluşturulur,
4. sahneler birleştirilip `output/demo-short.mp4` üretilir.

Bu ilk sürüm dış servis, API anahtarı, yapay ses veya otomatik YouTube yüklemesi kullanmaz. Amaç, ortamın doğru çalıştığını kanıtlayan yerel ve CI üzerinde test edilebilir bir taban sağlamaktır.

## Gereksinimler

- Python 3.11+
- FFmpeg 6+
- Linux/macOS; Windows için WSL önerilir

## Hızlı başlangıç

```bash
python -m shorts_automation validate examples/demo.json
python -m shorts_automation render examples/demo.json
```

Video varsayılan olarak `output/demo-short.mp4` konumuna yazılır. Farklı hedef için:

```bash
python -m shorts_automation render examples/demo.json --output output/ilk-video.mp4
```

## Proje yapısı

```text
.
├── .github/workflows/ci.yml       # doğrulama ve test
├── examples/demo.json             # örnek video tanımı
├── src/shorts_automation/         # CLI, doğrulama ve FFmpeg iş akışı
├── tests/                         # birim testleri
├── .env.example                   # sonraki entegrasyonlar için değişkenler
└── pyproject.toml                 # paket ve araç ayarları
```

## Video tanımı

Her iş JSON dosyasıdır. `scenes` dizisi en az bir sahne içermelidir; her sahnede ekranda gösterilecek `text` ve saniye cinsinden `duration` bulunur.

```json
{
  "slug": "demo-short",
  "title": "İlk Otomatik Short",
  "background_color": "0x111827",
  "text_color": "white",
  "scenes": [
    {"text": "Bir fikirle başla", "duration": 2.5}
  ]
}
```

Toplam süre 60 saniyeyi aşamaz. `slug` yalnızca küçük harf, sayı ve tire içerebilir.

## Yol haritası

1. Metinden konuşma (TTS) sağlayıcısı eklemek.
2. Stok veya üretilmiş görselleri sahnelere bağlamak.
3. Altyazı zamanlaması ve müzik miksajı eklemek.
4. YouTube Data API ile taslak yükleme eklemek.
5. İnsan onayı olmadan yayın yapmayan zamanlanmış üretim hattı kurmak.

YouTube kimlik bilgileri veya diğer sırlar depoya yazılmamalıdır. Gelecekte GitHub Actions kullanılırsa bunlar repository secrets olarak tanımlanmalıdır.
