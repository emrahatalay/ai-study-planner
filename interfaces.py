from abc import ABC, abstractmethod
from typing import List
from models import StudentPerformance, StudyPlan, Subject


class AIServiceInterface(ABC):
    """AI servisi için interface"""
    
    @abstractmethod
    async def generate_study_plan(
        self, 
        student_performance: StudentPerformance, 
        subjects_data: List[dict]  # PostgreSQL'den gelen id ve name verileri
    ) -> StudyPlan:
        """Öğrenci performansına göre çalışma planı oluşturur"""
        pass
    
    @abstractmethod
    def is_healthy(self) -> bool:
        """Servis sağlık durumunu kontrol eder"""
        pass
