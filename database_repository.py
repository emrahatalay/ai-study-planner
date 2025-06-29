from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Subject, Topic, StudentPerformance
from config import config
import logging


class DatabaseRepository:
    """PostgreSQL veritabanı işlemleri"""
    
    def __init__(self):
        self.database_url = config.database_url
        self.engine = None
        self.Session = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Veritabanı bağlantısını başlatır"""
        try:
            self.engine = create_engine(self.database_url, echo=False)
            self.Session = sessionmaker(bind=self.engine)
            logging.info("Database connection initialized successfully")
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            raise
    
    def get_all_subjects_with_topics(self) -> List[Subject]:
        """Tüm dersleri konularıyla birlikte getirir"""
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Dersler ve konuları birlikte getir
                    query = """
                    SELECT 
                        s."Id" as subject_id,
                        s."Name" as subject_name,
                        t."Id" as topic_id,
                        t."Name" as topic_name
                    FROM public."Subjects" s
                    LEFT JOIN public."Topics" t ON s."Id" = t."SubjectId"
                    ORDER BY s."Id", t."Id"
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    
                    # Verileri Subject ve Topic modeline dönüştür
                    subjects_dict = {}
                    for row in rows:
                        subject_id = row['subject_id']
                        if subject_id not in subjects_dict:
                            subjects_dict[subject_id] = {
                                'id': subject_id,
                                'name': row['subject_name'],
                                'topics': []
                            }
                        
                        if row['topic_id']:  # Konu varsa ekle
                            topic = Topic(
                                id=row['topic_id'],
                                name=row['topic_name']
                            )
                            subjects_dict[subject_id]['topics'].append(topic)
                    
                    # Subject modeline dönüştür
                    subjects = []
                    for subject_data in subjects_dict.values():
                        subject = Subject(
                            id=subject_data['id'],
                            name=subject_data['name'],
                            topics=subject_data['topics']
                        )
                        subjects.append(subject)
                    
                    return subjects
                    
        except Exception as e:
            logging.error(f"Error fetching subjects with topics: {e}")
            raise
    
    def get_subjects_for_ai(self) -> List[dict]:
        """AI için ders ve konu bilgilerини hazırlar (sadece id ve name)"""
        subjects = self.get_all_subjects_with_topics()
        ai_data = []
        
        for subject in subjects:
            subject_data = {
                'id': subject.id,
                'name': subject.name,
                'topics': [{'id': topic.id, 'name': topic.name} for topic in subject.topics]
            }
            ai_data.append(subject_data)
        
        return ai_data
    
    def get_student_performance(self, student_id: str) -> Optional[StudentPerformance]:
        """Öğrenci performansını getirir"""
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Öğrenci bilgilerini getir
                    student_query = """
                    SELECT "Id", "Name", "CreatedAt"
                    FROM public."Students"
                    WHERE "Id" = %s
                    """
                    cursor.execute(student_query, (student_id,))
                    student_row = cursor.fetchone()
                    
                    if not student_row:
                        return None
                    
                    # Öğrenci raporlarını getir
                    reports_query = """
                    SELECT "Subject", "Topics", "Score"
                    FROM public."StudentReports"
                    WHERE "StudentId" = %s
                    ORDER BY "CreatedAt" DESC
                    """
                    cursor.execute(reports_query, (student_id,))
                    reports_rows = cursor.fetchall()
                    
                    # Report modeline dönüştür
                    from models import Report
                    reports = [Report(
                        subject=row['subject'],
                        topics=row['topics'],
                        score=row['score']
                    ) for row in reports_rows]
                    
                    return StudentPerformance(
                        student_id=student_row['id'],
                        name=student_row['name'],
                        reports=reports,
                        created_at=student_row['createdat']
                    )
                    
        except Exception as e:
            logging.error(f"Error fetching student performance: {e}")
            raise

    def insert_sample_data(self):
        """Örnek veri ekler (test için)"""
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cursor:
                    # Önce mevcut verileri temizle
                    cursor.execute('DELETE FROM public."Topics"')
                    cursor.execute('DELETE FROM public."Subjects"')
                    cursor.execute('DELETE FROM public."StudentReports"')
                    cursor.execute('DELETE FROM public."Students"')
                    
                    # Örnek dersler (GUID'lerle)
                    subjects_data = [
                        ('11111111-1111-1111-1111-111111111111', 'Matematik'),
                        ('22222222-2222-2222-2222-222222222222', 'Fizik'),
                        ('33333333-3333-3333-3333-333333333333', 'Kimya'),
                        ('44444444-4444-4444-4444-444444444444', 'Biyoloji')
                    ]
                    
                    for subject_id, subject_name in subjects_data:
                        cursor.execute(
                            'INSERT INTO public."Subjects" ("Id", "Name") VALUES (%s, %s) ON CONFLICT ("Id") DO NOTHING',
                            (subject_id, subject_name)
                        )
                    
                    # Örnek konular (GUID'lerle)
                    topics_data = [
                        ('a1111111-1111-1111-1111-111111111111', 'Sayılar', '11111111-1111-1111-1111-111111111111'),
                        ('a2222222-2222-2222-2222-222222222222', 'Cebir', '11111111-1111-1111-1111-111111111111'),
                        ('a3333333-3333-3333-3333-333333333333', 'Geometri', '11111111-1111-1111-1111-111111111111'),
                        ('a4444444-4444-4444-4444-444444444444', 'İstatistik', '11111111-1111-1111-1111-111111111111'),
                        ('b1111111-1111-1111-1111-111111111111', 'Hareket', '22222222-2222-2222-2222-222222222222'),
                        ('b2222222-2222-2222-2222-222222222222', 'Kuvvet', '22222222-2222-2222-2222-222222222222'),
                        ('b3333333-3333-3333-3333-333333333333', 'Enerji', '22222222-2222-2222-2222-222222222222'),
                        ('b4444444-4444-4444-4444-444444444444', 'Elektrik', '22222222-2222-2222-2222-222222222222'),
                        ('c1111111-1111-1111-1111-111111111111', 'Atomlar', '33333333-3333-3333-3333-333333333333'),
                        ('c2222222-2222-2222-2222-222222222222', 'Moleküller', '33333333-3333-3333-3333-333333333333'),
                        ('c3333333-3333-3333-3333-333333333333', 'Reaksiyonlar', '33333333-3333-3333-3333-333333333333'),
                        ('c4444444-4444-4444-4444-444444444444', 'Asit-Baz', '33333333-3333-3333-3333-333333333333'),
                        ('d1111111-1111-1111-1111-111111111111', 'Hücre', '44444444-4444-4444-4444-444444444444'),
                        ('d2222222-2222-2222-2222-222222222222', 'Genetik', '44444444-4444-4444-4444-444444444444'),
                        ('d3333333-3333-3333-3333-333333333333', 'Ekoloji', '44444444-4444-4444-4444-444444444444'),
                        ('d4444444-4444-4444-4444-444444444444', 'Evrim', '44444444-4444-4444-4444-444444444444')
                    ]
                    
                    for topic_id, topic_name, subject_id in topics_data:
                        cursor.execute(
                            'INSERT INTO public."Topics" ("Id", "Name", "SubjectId") VALUES (%s, %s, %s) ON CONFLICT ("Id") DO NOTHING',
                            (topic_id, topic_name, subject_id)
                        )
                    
                    # Test öğrenci ekle
                    test_student_id = 'student1-1111-1111-1111-111111111111'
                    cursor.execute(
                        'INSERT INTO public."Students" ("Id", "Name") VALUES (%s, %s) ON CONFLICT ("Id") DO NOTHING',
                        (test_student_id, 'Ahmet Yılmaz')
                    )
                    
                    # Test rapor verileri ekle
                    test_reports = [
                        (test_student_id, "Matematik", "Sayılar, Cebir", 4),
                        (test_student_id, "Matematik", "Geometri", 7),
                        (test_student_id, "Fizik", "Hareket, Kuvvet", 5),
                        (test_student_id, "Kimya", "Atomlar", 8),
                        (test_student_id, "Biyoloji", "Hücre", 6)
                    ]
                    
                    for student_id, subject, topics, score in test_reports:
                        cursor.execute(
                            'INSERT INTO public."StudentReports" ("StudentId", "Subject", "Topics", "Score") VALUES (%s, %s, %s, %s)',
                            (student_id, subject, topics, score)
                        )
                    
                    conn.commit()
                    logging.info("Sample data inserted successfully")
                    
        except Exception as e:
            logging.error(f"Error inserting sample data: {e}")
            raise
    
    def create_database_tables(self):
        """Gerekli tabloları oluşturur (test için)"""
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cursor:
                    # Subjects tablosu
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public."Subjects" (
                        "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        "Name" VARCHAR(100) NOT NULL
                    )
                    """)
                    
                    # Topics tablosu
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public."Topics" (
                        "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        "Name" VARCHAR(100) NOT NULL,
                        "SubjectId" UUID REFERENCES public."Subjects"("Id")
                    )
                    """)
                    
                    # Students tablosu
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public."Students" (
                        "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        "Name" VARCHAR(100) NOT NULL,
                        "CreatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """)
                    
                    # Student reports tablosu
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public."StudentReports" (
                        "Id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        "StudentId" UUID REFERENCES public."Students"("Id"),
                        "Subject" VARCHAR(100) NOT NULL,
                        "Topics" TEXT NOT NULL,
                        "Score" INTEGER CHECK ("Score" >= 0 AND "Score" <= 10),
                        "CreatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """)
                    
                    conn.commit()
                    logging.info("Database tables created successfully")
                    
        except Exception as e:
            logging.error(f"Error creating database tables: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Veritabanı bağlantısını test eder"""
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    return True
        except Exception as e:
            logging.error(f"Database connection test failed: {e}")
            return False
