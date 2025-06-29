from typing import List
from models import Subject, Topic, StudentPerformance, Report


class DataRepository:
    """Veri deposu - gerçek uygulamada veritabanı olurdu"""
    
    def __init__(self):
        self._subjects = self._initialize_subjects()
        self._students = self._initialize_sample_students()
    
    def _initialize_subjects(self) -> List[Subject]:
        """Örnek ders ve konuları başlatır"""
        return [
            Subject(
                id=1,
                name="Matematik",
                topics=[
                    Topic(id=1, name="Sayılar"),
                    Topic(id=2, name="Cebir"),
                    Topic(id=3, name="Geometri"),
                    Topic(id=4, name="İstatistik")
                ]
            ),
            Subject(
                id=2,
                name="Fizik",
                topics=[
                    Topic(id=5, name="Hareket"),
                    Topic(id=6, name="Kuvvet"),
                    Topic(id=7, name="Enerji"),
                    Topic(id=8, name="Elektrik")
                ]
            ),
            Subject(
                id=3,
                name="Kimya",
                topics=[
                    Topic(id=9, name="Atomlar"),
                    Topic(id=10, name="Moleküller"),
                    Topic(id=11, name="Reaksiyonlar"),
                    Topic(id=12, name="Asit-Baz")
                ]
            ),
            Subject(
                id=4,
                name="Biyoloji",
                topics=[
                    Topic(id=13, name="Hücre"),
                    Topic(id=14, name="Genetik"),
                    Topic(id=15, name="Ekoloji"),
                    Topic(id=16, name="Evrim")
                ]
            )
        ]
    
    def _initialize_sample_students(self) -> List[StudentPerformance]:
        """Örnek öğrenci verilerini başlatır"""
        return [
            StudentPerformance(
                student_id="21d2a4dasd4as5dsa4",
                name="Emrah Atalay",
                reports=[
                    Report(subject="Matematik", topics="Sayılar", score=7),
                    Report(subject="Matematik", topics="Cebir", score=5),
                    Report(subject="Fizik", topics="Hareket", score=8),
                    Report(subject="Fizik", topics="Kuvvet", score=4),
                    Report(subject="Kimya", topics="Atomlar", score=9),
                    Report(subject="Biyoloji", topics="Hücre", score=6)
                ]
            ),
            StudentPerformance(
                student_id="31e3b5ebd5bs6esb5",
                name="Ayşe Yılmaz",
                reports=[
                    Report(subject="Matematik", topics="Geometri", score=9),
                    Report(subject="Matematik", topics="İstatistik", score=8),
                    Report(subject="Fizik", topics="Enerji", score=6),
                    Report(subject="Fizik", topics="Elektrik", score=7),
                    Report(subject="Kimya", topics="Reaksiyonlar", score=5),
                    Report(subject="Biyoloji", topics="Genetik", score=8)
                ]
            )
        ]
    
    def get_all_subjects(self) -> List[Subject]:
        """Tüm dersleri döndürür"""
        return self._subjects.copy()
    
    def get_subject_by_id(self, subject_id: int) -> Subject:
        """ID'ye göre ders döndürür"""
        for subject in self._subjects:
            if subject.id == subject_id:
                return subject
        raise ValueError(f"Subject with ID {subject_id} not found")
    
    def get_all_students(self) -> List[StudentPerformance]:
        """Tüm öğrencileri döndürür"""
        return self._students.copy()
    
    def get_student_by_id(self, student_id: str) -> StudentPerformance:
        """ID'ye göre öğrenci döndürür"""
        for student in self._students:
            if student.student_id == student_id:
                return student
        raise ValueError(f"Student with ID {student_id} not found")
    
    def add_student(self, student: StudentPerformance) -> None:
        """Yeni öğrenci ekler"""
        # Duplicate kontrolü
        for existing_student in self._students:
            if existing_student.student_id == student.student_id:
                raise ValueError(f"Student with ID {student.student_id} already exists")
        self._students.append(student)
