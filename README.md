# PostgreSQL & Gemini AI Çalışma Planı Üreticisi

Bu konsol uygulaması, PostgreSQL veritabanından ders ve konu bilgilerini alarak öğrencilerin performans verilerine dayanarak Gemini AI kullanarak kişiselleştirilmiş haftalık çalışma planları oluşturur.

## Özellikler

- 🎯 PostgreSQL veritabanı entegrasyonu
- 📊 Öğrenci performans analizi (10 üzerinden puanlama sistemi)
- 🤖 Gemini AI ile akıllı çalışma planı oluşturma
- 📚 Veritabanından dinamik ders ve konu yönetimi
- 🔢 Soru sayısı bazında çalışma programı (zor/kolay kavramları olmadan)
- � Ders ve konu ID'leriyle entegre çalışma
- 💡 Kişiselleştirilmiş öneriler
- 🎨 Renkli konsol arayüzü

## Teknolojiler

- **Python 3.12+**
- **PostgreSQL** - Veritabanı
- **Google Generative AI (Gemini)** - AI servisi
- **Pydantic** - Veri validasyonu
- **psycopg2-binary** - PostgreSQL bağlantısı
- **SQLAlchemy** - ORM
- **Colorama** - Konsol renklendirme
- **Python-dotenv** - Çevre değişkenleri yönetimi

## Kurulum

1. **Gereksinimler**

```bash
pip install -r requirements.txt
```

2. **PostgreSQL Veritabanı Kurulumu**

   - PostgreSQL'i kurun ve çalıştırın
   - Yeni bir veritabanı oluşturun (örn: `study_db`)

3. **Çevre Değişkenleri Yapılandırması**
   - `.env` dosyasını oluşturun ve aşağıdaki değerleri ayarlayın:

```env
# Gemini AI API Key
GEMINI_API_KEY=your_actual_api_key_here

# PostgreSQL Database Configuration
# Option 1: Complete connection string
DATABASE_URL=postgresql://username:password@localhost:5432/study_db

# Option 2: Individual parameters (if DATABASE_URL not provided)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=study_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

4. **Çalıştırma**

```bash
python main.py
```

## Kullanım

### Ana Menü Seçenekleri:

1. **PostgreSQL'den Ders ve Konuları Listele** - Veritabanından ders/konu yapısını görüntüler
2. **AI ile Çalışma Planı Oluştur** - PostgreSQL verilerini kullanarak AI destekli plan oluşturma
3. **Veritabanı İşlemlerini Test Et** - PostgreSQL bağlantısını ve veri işlemlerini test eder
4. **AI'ya Gönderilen Veri Formatını Göster** - AI'ya gönderilen JSON formatını görüntüler
5. **Çıkış** - Uygulamayı kapatır

### Veritabanı Yapısı

**Tablolar:**

```sql
-- Dersler
CREATE TABLE public."Subjects" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "Name" VARCHAR(100) NOT NULL
);

-- Konular
CREATE TABLE public."Topics" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "Name" VARCHAR(100) NOT NULL,
    "SubjectId" UUID REFERENCES public."Subjects"("Id")
);

-- Öğrenciler
CREATE TABLE public."Students" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "Name" VARCHAR(100) NOT NULL,
    "CreatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Öğrenci raporları
CREATE TABLE public."StudentReports" (
    "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "StudentId" UUID REFERENCES public."Students"("Id"),
    "Subject" VARCHAR(100) NOT NULL,
    "Topics" TEXT NOT NULL,
    "Score" INTEGER CHECK ("Score" >= 0 AND "Score" <= 10),
    "CreatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### AI'ya Gönderilen Veri Formatı

```json
[
  {
    "id": "11111111-1111-1111-1111-111111111111",
    "name": "Matematik",
    "topics": [
      { "id": "a1111111-1111-1111-1111-111111111111", "name": "Sayılar" },
      { "id": "a2222222-2222-2222-2222-222222222222", "name": "Cebir" }
    ]
  }
]
```

**Öğrenci Performansı:**

````json
{
  "student_id": "student1-1111-1111-1111-111111111111",
  "name": "Ahmet Yılmaz",
  "reports": [
    {
      "subject": "Matematik",
      "topics": "Sayılar, Cebir",
      "score": 4
    }
  ]
}

**AI'dan Dönen Çalışma Planı Formatı:**

```json
{
  "week_number": 1,
  "total_questions": 180,
  "subject_plans": [
    {
      "subject_id": "11111111-1111-1111-1111-111111111111",
      "subject_name": "Matematik",
      "total_questions": 60,
      "topics": [
        {
          "topic_id": "a1111111-1111-1111-1111-111111111111",
          "topic_name": "Sayılar",
          "question_count": 20
        },
        {
          "topic_id": "a2222222-2222-2222-2222-222222222222",
          "topic_name": "Cebir",
          "question_count": 25
        }
      ]
    }
  ],
  "weak_subjects": ["Matematik", "Fizik"],
  "recommendations": [
    "Zayıf konularda günde en az 20 soru çöz",
    "Yanlış yaptığın soruları tekrar et"
  ]
}
````

## Mimari

Proje SOLID prensipleri ve Clean Code yaklaşımını benimser:

### Katmanlar:

- **Models** (`models.py`) - Veri modelleri (Pydantic)
- **Interfaces** (`interfaces.py`) - Servis arayüzleri
- **Services** (`gemini_service.py`, `study_plan_service.py`) - İş mantığı
- **Database Repository** (`database_repository.py`) - PostgreSQL veri erişimi
- **UI** (`console_ui.py`) - Kullanıcı arayüzü
- **Configuration** (`config.py`) - Uygulama ve veritabanı ayarları

### Design Patterns:

- **Repository Pattern** - Veri erişimi
- **Service Layer Pattern** - İş mantığı ayrımı
- **Dependency Injection** - Gevşek bağlılık

### Önemli Özellikler:

- **PostgreSQL Entegrasyonu** - Ders ve konu verileri veritabanından alınır
- **ID Tabanlı Çalışma** - AI, veritabanı ID'lerini kullanarak sonuç üretir
- **Soru Sayısı Odaklı** - Zor/kolay gibi kavramlar kullanılmaz, sadece soru sayısı
- **Dinamik Veri Yönetimi** - Dersler ve konular veritabanından dinamik olarak yönetilir
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
