from abc import ABC, abstractmethod
from typing import List
from models import StudentPerformance, StudyPlan, Subject


class AIServiceInterface(ABC):
    """AI servisi için interface"""
    
    @abstractmethod
    async def generate_study_plan(
        self, 
        student_performance: StudentPerformance, 
        subjects: List[Subject]
    ) -> StudyPlan:
        """Öğrenci performansına göre çalışma planı oluşturur"""
        pass
    
    @abstractmethod
    def is_healthy(self) -> bool:
        """Servis sağlık durumunu kontrol eder"""
        pass
