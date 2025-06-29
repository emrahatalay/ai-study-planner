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
        """Çalışma planını yazdırır"""
        ConsoleUI.print_header(f"{study_plan.student_name} - ÇALIŞMA PLANI")
        
        print(f"{Fore.CYAN}Hafta: {study_plan.week_number}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Toplam Soru Sayısı: {study_plan.total_questions} soru{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Plan Tarihi: {study_plan.created_at.strftime('%d/%m/%Y %H:%M')}{Style.RESET_ALL}")
        
        # Zayıf konuları göster
        if study_plan.weak_subjects:
            print(f"\n{Fore.RED}🔴 Zayıf Konular:{Style.RESET_ALL}")
            for subject in study_plan.weak_subjects:
                print(f"   • {subject}")
        
        # Günlük planları göster
        print(f"\n{Fore.YELLOW}📅 Günlük Çalışma Planı:{Style.RESET_ALL}")
        for daily_plan in study_plan.daily_plans:
            print(f"\n{Fore.GREEN}📅 {daily_plan.get('day', 'Bilinmeyen Gün')}{Style.RESET_ALL}")
            
            subjects_data = daily_plan.get('subjects', [])
            if subjects_data:
                total_daily_questions = sum(s.get('question_count', 0) for s in subjects_data)
                print(f"   Toplam: {total_daily_questions} soru")
                
                for subject_data in subjects_data:
                    subject_name = subject_data.get('subject', 'Bilinmeyen')
                    topic_name = subject_data.get('topic', 'Bilinmeyen')
                    question_count = subject_data.get('question_count', 0)
                    question_types = subject_data.get('question_types', [])
                    difficulty_levels = subject_data.get('difficulty_levels', [])
                    
                    print(f"   📖 {subject_name} - {topic_name} ({question_count} soru)")
                    
                    if question_types:
                        print(f"      🎯 Soru Tipleri:")
                        for q_type in question_types:
                            print(f"         • {q_type}")
                    
                    if difficulty_levels:
                        print(f"      📊 Zorluk Seviyeleri:")
                        for difficulty in difficulty_levels:
                            print(f"         • {difficulty}")
            else:
                print("   Çalışma planı mevcut değil")
        
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
        ConsoleUI.print_header("GEMİNİ AI ÇALIŞMA PLANI ÜRETİCİSİ")
        print(f"{Fore.YELLOW}1.{Style.RESET_ALL} Tüm öğrencileri listele")
        print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Tüm dersleri ve konuları listele")
        print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Öğrenci için çalışma planı oluştur")
        print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Çıkış")
        print()
    
    @staticmethod
    def wait_for_enter():
        """Kullanıcının Enter tuşuna basmasını bekler"""
        input(f"\n{Fore.LIGHTBLACK_EX}Devam etmek için Enter tuşuna basın...{Style.RESET_ALL}")
        print("\n" * 2)
