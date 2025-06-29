from typing import List
from models import StudentPerformance, StudyPlan, Subject
from interfaces import AIServiceInterface
from database_repository import DatabaseRepository


class StudyPlanService:
    """Çalışma planı servisi - business logic"""
    
    def __init__(self, ai_service: AIServiceInterface, db_repository: DatabaseRepository):
        self.ai_service = ai_service
        self.db_repository = db_repository
    
    async def generate_study_plan_for_student(self, student_id: str) -> StudyPlan:
        """Öğrenci için çalışma planı oluşturur"""
        # PostgreSQL'den öğrenci verilerini al
        student_performance = self.db_repository.get_student_performance(student_id)
        
        if not student_performance:
            raise ValueError(f"Student with ID {student_id} not found")
        
        # PostgreSQL'den ders ve konu verilerini al (sadece id ve name)
        subjects_data = self.db_repository.get_subjects_for_ai()
        
        # Öğrenci performansını analiz et
        analysis = self._analyze_student_performance(student_performance)
        
        # AI'dan çalışma planı oluşturmasını iste
        study_plan = await self.ai_service.generate_study_plan(student_performance, subjects_data)
        
        return study_plan
    
    def get_all_subjects_from_db(self) -> List[dict]:
        """PostgreSQL'den tüm dersleri döndürür"""
        return self.db_repository.get_subjects_for_ai()
    
    def get_all_subjects(self) -> List[Subject]:
        """Tüm dersleri Subject modeli olarak döndürür"""
        return self.db_repository.get_all_subjects_with_topics()
    
    def test_database_connection(self) -> bool:
        """Veritabanı bağlantısını test eder"""
        return self.db_repository.test_connection()
    
    def _analyze_student_performance(self, student_performance: StudentPerformance) -> dict:
        """Öğrenci performansını analiz eder"""
        total_score = sum(report.score for report in student_performance.reports)
        average_score = total_score / len(student_performance.reports) if student_performance.reports else 0
        
        weak_subjects = []
        strong_subjects = []
        
        # Ders bazında ortalama hesapla
        subject_scores = {}
        for report in student_performance.reports:
            if report.subject not in subject_scores:
                subject_scores[report.subject] = []
            subject_scores[report.subject].append(report.score)
        
        for subject, scores in subject_scores.items():
            avg_score = sum(scores) / len(scores)
            if avg_score < 6:
                weak_subjects.append(subject)
            elif avg_score >= 8:
                strong_subjects.append(subject)
        
        return {
            "overall_average": average_score,
            "weak_subjects": weak_subjects,
            "strong_subjects": strong_subjects,
            "total_reports": len(student_performance.reports)
        }
