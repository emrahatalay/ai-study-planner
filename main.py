import asyncio
import sys
from gemini_service import GeminiAIService
from repository import DataRepository
from study_plan_service import StudyPlanService
from console_ui import ConsoleUI


class StudyPlanApplication:
    """Ana uygulama sınıfı"""
    
    def __init__(self):
        """Uygulama bileşenlerini başlatır"""
        self.ui = ConsoleUI()
        self.repository = DataRepository()
        self.ai_service = GeminiAIService()
        self.study_plan_service = StudyPlanService(self.ai_service, self.repository)
    
    async def run(self):
        """Uygulamayı çalıştırır"""
        # Servis sağlık kontrolü
        if not self.ai_service.is_healthy():
            self.ui.print_error("Gemini AI servisi yapılandırılmamış!")
            self.ui.print_warning("Lütfen .env dosyasında GEMINI_API_KEY değerini ayarlayın.")
            return
        
        self.ui.print_success("Gemini AI servisi başarıyla bağlandı!")
        
        while True:
            try:
                self.ui.print_menu()
                choice = self.ui.get_user_choice(4)
                
                if choice == 1:
                    await self._list_students()
                elif choice == 2:
                    await self._list_subjects()
                elif choice == 3:
                    await self._generate_study_plan()
                elif choice == 4:
                    self.ui.print_info("Uygulama kapatılıyor...")
                    break
                
            except KeyboardInterrupt:
                self.ui.print_info("\nUygulama kullanıcı tarafından durduruldu.")
                break
            except Exception as e:
                self.ui.print_error(f"Beklenmeyen hata: {e}")
                self.ui.wait_for_enter()
    
    async def _list_students(self):
        """Tüm öğrencileri listeler"""
        try:
            students = self.study_plan_service.get_all_students()
            self.ui.print_students(students)
            self.ui.wait_for_enter()
        except Exception as e:
            self.ui.print_error(f"Öğrenci listesi alınamadı: {e}")
            self.ui.wait_for_enter()
    
    async def _list_subjects(self):
        """Tüm dersleri ve konuları listeler"""
        try:
            subjects = self.study_plan_service.get_all_subjects()
            self.ui.print_subjects(subjects)
            self.ui.wait_for_enter()
        except Exception as e:
            self.ui.print_error(f"Ders listesi alınamadı: {e}")
            self.ui.wait_for_enter()
    
    async def _generate_study_plan(self):
        """Öğrenci için çalışma planı oluşturur"""
        try:
            # Öğrenci listesini göster
            students = self.study_plan_service.get_all_students()
            self.ui.print_students(students)
            
            # Öğrenci seçimi
            choice = self.ui.get_user_choice(len(students))
            selected_student = students[choice - 1]
            
            self.ui.print_info(f"{selected_student.name} için soru bazlı çalışma planı oluşturuluyor...")
            self.ui.print_warning("Bu işlem 10-30 saniye sürebilir, lütfen bekleyin...")
            
            # AI'dan çalışma planı oluştur
            study_plan = await self.study_plan_service.generate_study_plan_for_student(
                selected_student.student_id
            )
            
            # Planı göster
            self.ui.print_study_plan(study_plan)
            self.ui.wait_for_enter()
            
        except Exception as e:
            self.ui.print_error(f"Çalışma planı oluşturulamadı: {e}")
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