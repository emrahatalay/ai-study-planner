from pydantic import BaseModel, validator, Field
from typing import List, Optional
from datetime import datetime


class Topic(BaseModel):
    """Ders konusu modeli"""
    id: int
    name: str


class Subject(BaseModel):
    """Ders modeli"""
    id: int
    name: str
    topics: List[Topic]


class Report(BaseModel):
    """Öğrenci başarı raporu modeli"""
    subject: str
    topics: str
    score: int
    
    @validator('score')
    def validate_score(cls, v):
        if not (0 <= v <= 10):
            raise ValueError("Score must be between 0 and 10")
        return v


class StudentPerformance(BaseModel):
    """Öğrenci performans modeli"""
    student_id: str
    name: str
    reports: List[Report]
    created_at: Optional[datetime] = Field(default_factory=datetime.now)


class StudyPlan(BaseModel):
    """Çalışma planı modeli"""
    student_id: str
    student_name: str
    week_number: int
    total_questions: int  # Toplam soru sayısı
    daily_plans: List[dict]
    weak_subjects: List[str]
    recommendations: List[str]
    created_at: datetime
