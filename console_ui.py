import json
from typing import List
from colorama import init, Fore, Style
from models import StudentPerformance, StudyPlan, Subject

# Colorama'yı başlat (Windows için)
init()


class ConsoleUI:
    """Konsol arayüzü yardımcı sınıfı"""
    
    @staticmethod
    def print_header(title: str):
        """Başlık yazdırır"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{title.center(50)}")
        print(f"{'='*50}{Style.RESET_ALL}\n")
    
    @staticmethod
    def print_success(message: str):
        """Başarı mesajı yazdırır"""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_error(message: str):
        """Hata mesajı yazdırır"""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_warning(message: str):
        """Uyarı mesajı yazdırır"""
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_info(message: str):
        """Bilgi mesajı yazdırır"""
        print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def print_students(students: List[StudentPerformance]):
        """Öğrenci listesini yazdırır"""
        ConsoleUI.print_header("ÖĞRENCI LİSTESİ")
        
        for i, student in enumerate(students, 1):
            print(f"{Fore.YELLOW}{i}. {student.name} (ID: {student.student_id}){Style.RESET_ALL}")
            
            # Performans özetini göster
            if student.reports:
                total_score = sum(report.score for report in student.reports)
                avg_score = total_score / len(student.reports)
                color = Fore.GREEN if avg_score >= 7 else Fore.YELLOW if avg_score >= 5 else Fore.RED
                print(f"   Ortalama: {color}{avg_score:.1f}/10{Style.RESET_ALL}")
                
                # Zayıf konuları göster
                weak_reports = [r for r in student.reports if r.score < 6]
                if weak_reports:
                    print(f"   Zayıf konular: {Fore.RED}{', '.join([f'{r.subject}-{r.topics}' for r in weak_reports])}{Style.RESET_ALL}")
            print()
    
    @staticmethod
    def print_subjects(subjects: List[Subject]):
        """Ders listesini yazdırır"""
        ConsoleUI.print_header("DERS VE KONULAR")
        
        for subject in subjects:
            print(f"{Fore.CYAN}📚 {subject.name}{Style.RESET_ALL}")
            for topic in subject.topics:
                print(f"   • {topic.name}")
            print()
    
    @staticmethod
    def print_study_plan(study_plan: StudyPlan):
        """Çalışma planını yazdırır (PostgreSQL ID'leriyle)"""
        ConsoleUI.print_header(f"{study_plan.student_name} - ÇALIŞMA PLANI")
        
        print(f"{Fore.CYAN}Hafta: {study_plan.week_number}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Toplam Soru Sayısı: {study_plan.total_questions} soru{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Plan Tarihi: {study_plan.created_at.strftime('%d/%m/%Y %H:%M')}{Style.RESET_ALL}")
        
        # Zayıf konuları göster
        if study_plan.weak_subjects:
            print(f"\n{Fore.RED}🔴 Zayıf Konular:{Style.RESET_ALL}")
            for subject in study_plan.weak_subjects:
                print(f"   • {subject}")
        
        # Ders bazında soru dağılımını göster
        print(f"\n{Fore.YELLOW}� Ders Bazında Soru Dağılımı:{Style.RESET_ALL}")
        for subject_plan in study_plan.subject_plans:
            subject_id = subject_plan.get('subject_id', 'N/A')
            subject_name = subject_plan.get('subject_name', 'Bilinmeyen')
            total_questions = subject_plan.get('total_questions', 0)
            
            print(f"\n{Fore.GREEN}📖 {subject_name} (ID: {subject_id}) - {total_questions} soru{Style.RESET_ALL}")
            
            topics = subject_plan.get('topics', [])
            for topic in topics:
                topic_id = topic.get('topic_id', 'N/A')
                topic_name = topic.get('topic_name', 'Bilinmeyen')
                question_count = topic.get('question_count', 0)
                
                print(f"   • {topic_name} (ID: {topic_id}): {question_count} soru")
        
        # Önerileri göster
        if study_plan.recommendations:
            print(f"\n{Fore.BLUE}💡 Öneriler:{Style.RESET_ALL}")
            for recommendation in study_plan.recommendations:
                print(f"   • {recommendation}")
        
        print()
    
    @staticmethod
    def get_user_choice(max_option: int) -> int:
        """Kullanıcıdan seçim alır"""
        while True:
            try:
                choice = int(input(f"{Fore.CYAN}Seçiminizi yapın (1-{max_option}): {Style.RESET_ALL}"))
                if 1 <= choice <= max_option:
                    return choice
                else:
                    ConsoleUI.print_error(f"Lütfen 1-{max_option} arasında bir sayı girin.")
            except ValueError:
                ConsoleUI.print_error("Geçerli bir sayı girin.")
    
    @staticmethod
    def print_menu():
        """Ana menüyü yazdırır"""
        ConsoleUI.print_header("POSTGRESQL & AI ENTEGRASYON ÇALIŞMA PLANI")
        print(f"{Fore.YELLOW}1.{Style.RESET_ALL} PostgreSQL'den Ders ve Konuları Listele")
        print(f"{Fore.YELLOW}2.{Style.RESET_ALL} AI ile Çalışma Planı Oluştur")
        print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Veritabanı İşlemlerini Test Et")
        print(f"{Fore.YELLOW}4.{Style.RESET_ALL} AI'ya Gönderilen Veri Formatını Göster")
        print(f"{Fore.YELLOW}5.{Style.RESET_ALL} Çıkış")
        print()
    
    @staticmethod
    def wait_for_enter():
        """Kullanıcının Enter tuşuna basmasını bekler"""
        input(f"\n{Fore.LIGHTBLACK_EX}Devam etmek için Enter tuşuna basın...{Style.RESET_ALL}")
        print("\n" * 2)
