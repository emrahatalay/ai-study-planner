# Gemini AI Çalışma Planı Üreticisi

Bu konsol uygulaması, öğrencilerin performans verilerine dayanarak Gemini AI kullanarak kişiselleştirilmiş haftalık çalışma planları oluşturur.

## Özellikler

- 🎯 Öğrenci performans analizi (10 üzerinden puanlama sistemi)
- 🤖 Gemini AI ile akıllı çalışma planı oluşturma
- 📚 Çoklu ders ve konu desteği (Matematik, Fizik, Kimya, Biyoloji)
- � Soru sayısı bazında günlük çalışma programı
- 🎯 Zorluk seviyelerine göre soru dağılımı
- 💡 Kişiselleştirilmiş öneriler
- 🎨 Renkli konsol arayüzü

## Teknolojiler

- **Python 3.12+**
- **Google Generative AI (Gemini)** - AI servisi
- **Pydantic** - Veri validasyonu
- **Colorama** - Konsol renklendirme
- **Python-dotenv** - Çevre değişkenleri yönetimi

## Kurulum

1. **Gereksinimler**

```bash
pip install -r requirements.txt
```

2. **API Anahtarı Yapılandırması**
   - `.env` dosyasında `GEMINI_API_KEY` değerini ayarlayın:

```
GEMINI_API_KEY=your_actual_api_key_here
```

3. **Çalıştırma**

```bash
python main.py
```

## Kullanım

### Ana Menü Seçenekleri:

1. **Tüm öğrencileri listele** - Kayıtlı öğrencileri ve performanslarını görüntüler
2. **Tüm dersleri ve konuları listele** - Mevcut ders/konu yapısını gösterir
3. **Öğrenci için çalışma planı oluştur** - AI destekli plan oluşturma
4. **Çıkış** - Uygulamayı kapatır

### Veri Yapısı

**Öğrenci Performansı:**

```json
{
  "student_id": "21d2a4dasd4as5dsa4",
  "name": "Emrah Atalay",
  "reports": [
    {
      "subject": "Matematik",
      "topics": "Sayılar",
      "score": 7
    }
  ]
}
```

**Ders Yapısı:**

```json
{
  "id": 1,
  "name": "Matematik",
  "topics": [
    {
      "id": 1,
      "name": "Sayılar"
    }
  ]
}
```

## Mimari

Proje SOLID prensipleri ve Clean Code yaklaşımını benimser:

### Katmanlar:

- **Models** (`models.py`) - Veri modelleri (Pydantic)
- **Interfaces** (`interfaces.py`) - Servis arayüzleri
- **Services** (`gemini_service.py`, `study_plan_service.py`) - İş mantığı
- **Repository** (`repository.py`) - Veri erişim katmanı
- **UI** (`console_ui.py`) - Kullanıcı arayüzü
- **Configuration** (`config.py`) - Uygulama ayarları

### Design Patterns:

- **Repository Pattern** - Veri erişimi
- **Service Layer Pattern** - İş mantığı ayrımı
- **Dependency Injection** - Gevşek bağlılık
- **Strategy Pattern** - AI servisi değiştirilebilirliği

## AI Çalışma Planı İşleyişi

1. **Performans Analizi**: Öğrencinin son raporları analiz edilir
2. **Zayıf Alanlar Belirlenir**: 6 puan altı konular tespit edilir
3. **Güçlü Alanlar Belirlenir**: 8 puan üstü konular tespit edilir
4. **Haftalık Plan Oluşturulur**: Zayıf alanlara daha fazla soru atanır
5. **Soru Dağılımı**: Her konu için uygun soru sayısı ve tipi belirlenir
6. **Zorluk Seviyeleri**: Kolay, orta, zor seviyelerde soru dağılımı
7. **Öneriler**: Kişiselleştirilmiş çalışma önerileri

## Örnek Çıktı

```
📅 Pazartesi
   Toplam: 25 soru
   📖 Matematik - Cebir (15 soru)
      🎯 Soru Tipleri:
         • Temel işlemler
         • Problem çözme
         • Uygulamalı sorular
      📊 Zorluk Seviyeleri:
         • Kolay: 8 soru
         • Orta: 5 soru
         • Zor: 2 soru
   📖 Fizik - Kuvvet (10 soru)
      🎯 Soru Tipleri:
         • Temel kavramlar
         • Formül uygulamaları

💡 Öneriler:
   • Zayıf konularda günde en az 20 soru çöz
   • Yanlış yaptığın soruları tekrar et
```

## Geliştirme

Yeni özellikler eklemek için:

1. **Yeni Model** - `models.py` dosyasına ekleyin
2. **Yeni Servis** - Interface tanımlayıp implement edin
3. **UI Güncellemesi** - `console_ui.py` dosyasını güncelleyin
4. **Ana Akış** - `main.py` dosyasında yeni menü seçeneği ekleyin

## Hata Ayıklama

**Gemini AI Bağlantı Hatası:**

- API anahtarının doğru olduğundan emin olun
- İnternet bağlantınızı kontrol edin
- API kullanım limitinizi kontrol edin

**JSON Parse Hatası:**

- AI yanıtı beklenmedik format döndürüyor olabilir
- Prompt güncelleme gerekebilir
