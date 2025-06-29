import asyncio
import sys
import logging
from gemini_service import GeminiAIService
from database_repository import DatabaseRepository
from study_plan_service import StudyPlanService
from console_ui import ConsoleUI

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class StudyPlanApplication:
    """Ana uygulama sınıfı"""
    
    def __init__(self):
        """Uygulama bileşenlerini başlatır"""
        self.ui = ConsoleUI()
        self.db_repository = DatabaseRepository()
        self.ai_service = GeminiAIService()
        self.study_plan_service = StudyPlanService(self.ai_service, self.db_repository)
    
    async def run(self):
        """Uygulamayı çalıştırır"""
        # Veritabanı bağlantısını test et
        self.ui.print_info("Veritabanı bağlantısı test ediliyor...")
        if not self.study_plan_service.test_database_connection():
            self.ui.print_error("PostgreSQL veritabanına bağlanılamadı!")
            self.ui.print_warning("Lütfen .env dosyasında veritabanı bilgilerini kontrol edin.")
            self.ui.print_info("Gerekli environment değişkenleri:")
            self.ui.print_info("- DATABASE_URL veya DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
            return
        
        self.ui.print_success("PostgreSQL veritabanına başarıyla bağlandı!")
        
        # Servis sağlık kontrolü
        if not self.ai_service.is_healthy():
            self.ui.print_error("Gemini AI servisi yapılandırılmamış!")
            self.ui.print_warning("Lütfen .env dosyasında GEMINI_API_KEY değerini ayarlayın.")
            return
        
        self.ui.print_success("Gemini AI servisi başarıyla bağlandı!")
        
        # Veritabanı tablolarını ve örnek verileri oluştur
        try:
            self.db_repository.create_database_tables()
            self.db_repository.insert_sample_data()
            self.ui.print_success("Veritabanı tabloları ve örnek veriler hazırlandı!")
        except Exception as e:
            self.ui.print_warning(f"Veritabanı hazırlama uyarısı: {e}")
        
        while True:
            try:
                self.ui.print_menu()
                choice = self.ui.get_user_choice(5)  # Menü seçeneği sayısını artırdık
                
                if choice == 1:
                    await self._list_subjects_from_db()
                elif choice == 2:
                    await self._generate_study_plan()
                elif choice == 3:
                    await self._test_database_operations()
                elif choice == 4:
                    await self._show_ai_subjects_data()
                elif choice == 5:
                    self.ui.print_info("Uygulama kapatılıyor...")
                    break
                
            except KeyboardInterrupt:
                self.ui.print_info("\nUygulama kullanıcı tarafından durduruldu.")
                break
            except Exception as e:
                self.ui.print_error(f"Beklenmeyen hata: {e}")
                self.ui.wait_for_enter()
    
    async def _list_subjects_from_db(self):
        """PostgreSQL'den tüm dersleri ve konuları listeler"""
        try:
            subjects = self.study_plan_service.get_all_subjects()
            self.ui.print_subjects(subjects)
            self.ui.wait_for_enter()
        except Exception as e:
            self.ui.print_error(f"Veritabanından ders listesi alınamadı: {e}")
            self.ui.wait_for_enter()
    
    async def _show_ai_subjects_data(self):
        """AI'ya gönderilen ders verilerini gösterir"""
        try:
            subjects_data = self.study_plan_service.get_all_subjects_from_db()
            self.ui.print_info("AI'ya gönderilen ders ve konu verileri:")
            import json
            print(json.dumps(subjects_data, ensure_ascii=False, indent=2))
            self.ui.wait_for_enter()
        except Exception as e:
            self.ui.print_error(f"AI veri formatı alınamadı: {e}")
            self.ui.wait_for_enter()
    
    async def _test_database_operations(self):
        """Veritabanı işlemlerini test eder"""
        try:
            self.ui.print_info("Veritabanı işlemleri test ediliyor...")
            
            # Test öğrenci verisi kontrol et (GUID formatında)
            student_id = "student1-1111-1111-1111-111111111111"
            performance = self.db_repository.get_student_performance(student_id)
            
            if performance:
                self.ui.print_success(f"Test öğrenci bulundu: {performance.name}")
                self.ui.print_info(f"Toplam rapor sayısı: {len(performance.reports)}")
            else:
                self.ui.print_warning("Test öğrenci bulunamadı. Örnek veri ekleniyor...")
                # Burada test verisi ekleyebilirsiniz
            
            self.ui.wait_for_enter()
        except Exception as e:
            self.ui.print_error(f"Veritabanı test hatası: {e}")
            self.ui.wait_for_enter()
    
    async def _generate_study_plan(self):
        """Öğrenci için çalışma planı oluşturur"""
        try:
            # Test öğrenci ID'si (GUID formatında)
            student_id = "student1-1111-1111-1111-111111111111"
            
            # Test öğrenci performansını kontrol et
            performance = self.db_repository.get_student_performance(student_id)
            if not performance:
                self.ui.print_warning("Test öğrenci bulunamadı. Lütfen uygulama menüsünden 'Veritabanı İşlemlerini Test Et' seçeneğini çalıştırın.")
                return
            
            if not performance:
                self.ui.print_error("Test öğrenci oluşturulamadı!")
                return
            
            self.ui.print_info(f"{performance.name} için PostgreSQL verilerinden soru bazlı çalışma planı oluşturuluyor...")
            self.ui.print_warning("Bu işlem 10-30 saniye sürebilir, lütfen bekleyin...")
            
            # AI'dan çalışma planı oluştur
            study_plan = await self.study_plan_service.generate_study_plan_for_student(student_id)
            
            # Planı göster
            self.ui.print_study_plan(study_plan)
            self.ui.wait_for_enter()
            
        except Exception as e:
            self.ui.print_error(f"Çalışma planı oluşturulamadı: {e}")
            import traceback
            print(traceback.format_exc())
            self.ui.wait_for_enter()
    

async def main():
    """Ana fonksiyon"""
    try:
        app = StudyPlanApplication()
        await app.run()
    except Exception as e:
        print(f"Uygulama başlatılamadı: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Windows için event loop policy ayarla
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(main())