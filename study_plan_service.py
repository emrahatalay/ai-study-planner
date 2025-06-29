from typing import List
from models import StudentPerformance, StudyPlan, Subject
from interfaces import AIServiceInterface
from repository import DataRepository


class StudyPlanService:
    """Çalışma planı servisi - business logic"""
    
    def __init__(self, ai_service: AIServiceInterface, repository: DataRepository):
        self.ai_service = ai_service
        self.repository = repository
    
    async def generate_study_plan_for_student(self, student_id: str) -> StudyPlan:
        """Öğrenci için çalışma planı oluşturur"""
        # Öğrenci verilerini al
        student_performance = self.repository.get_student_by_id(student_id)
        
        # Tüm dersleri al
        subjects = self.repository.get_all_subjects()
        
        # Öğrenci performansını analiz et
        analysis = self._analyze_student_performance(student_performance)
        
        # AI'dan çalışma planı oluşturmasını iste
        study_plan = await self.ai_service.generate_study_plan(student_performance, subjects)
        
        return study_plan
    
    def get_all_students(self) -> List[StudentPerformance]:
        """Tüm öğrencileri döndürür"""
        return self.repository.get_all_students()
    
    def get_all_subjects(self) -> List[Subject]:
        """Tüm dersleri döndürür"""
        return self.repository.get_all_subjects()
    
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
