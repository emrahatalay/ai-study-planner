import google.generativeai as genai
import json
from typing import List
from datetime import datetime
from interfaces import AIServiceInterface
from models import StudentPerformance, StudyPlan, Subject
from config import config


class GeminiAIService(AIServiceInterface):
    """Gemini AI servisi implementasyonu"""
    
    def __init__(self):
        """Gemini AI servisini başlatır"""
        try:
            genai.configure(api_key=config.gemini_api_key)
            self.model = genai.GenerativeModel(config.model_name)
            self._is_configured = True
        except Exception as e:
            print(f"Gemini AI yapılandırma hatası: {e}")
            self._is_configured = False
    
    def is_healthy(self) -> bool:
        """Servis sağlık durumunu kontrol eder"""
        return self._is_configured
    
    async def generate_study_plan(
        self, 
        student_performance: StudentPerformance, 
        subjects: List[Subject]
    ) -> StudyPlan:
        """Öğrenci performansına göre çalışma planı oluşturur"""
        if not self.is_healthy():
            raise Exception("Gemini AI servisi yapılandırılmamış")
        
        prompt = self._create_prompt(student_performance, subjects)
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text, student_performance)
        except Exception as e:
            raise Exception(f"Gemini AI isteği başarısız: {e}")
    
    def _create_prompt(self, student_performance: StudentPerformance, subjects: List[Subject]) -> str:
        """AI için prompt oluşturur"""
        
        subjects_json = json.dumps([{
            "id": subject.id,
            "name": subject.name,
            "topics": [{"id": topic.id, "name": topic.name} for topic in subject.topics]
        } for subject in subjects], ensure_ascii=False, indent=2)
        
        reports_json = json.dumps([{
            "subject": report.subject,
            "topics": report.topics,
            "score": report.score
        } for report in student_performance.reports], ensure_ascii=False, indent=2)
        
        prompt = f"""
Sen bir eğitim uzmanısın. Aşağıdaki veriler doğrultusunda bir öğrenci için bir haftalık çalışma planı oluştur.

Öğrenci Bilgileri:
- Ad: {student_performance.name}
- ID: {student_performance.student_id}

Mevcut Dersler ve Konular:
{subjects_json}

Son 3 Haftalık Performans Raporu (10 üzerinden puanlama):
{reports_json}

Görevlerin:
1. Zayıf konuları (6 puan altı) belirle
2. Güçlü konuları (8 puan üstü) belirle
3. Haftalık toplam çözülecek soru sayısını öner (100-300 soru arası)
4. Her gün için detaylı çalışma programı oluştur (soru sayısı bazında)
5. Öğrenciye özel öneriler ver

ÖNEMLI: Çalışma planını saat bazında değil, çözülecek soru sayısı bazında oluştur.
- Zayıf konulara daha fazla soru ayır
- Güçlü konularda tekrar için az soru ver
- Her konu için uygun soru tiplerini belirt

Lütfen yanıtını aşağıdaki JSON formatında ver:

{{
    "week_number": 1,
    "total_questions": 180,
    "daily_plans": [
        {{
            "day": "Pazartesi",
            "subjects": [
                {{
                    "subject": "Matematik",
                    "topic": "Sayılar",
                    "question_count": 15,
                    "question_types": ["Temel işlemler", "Problem çözme", "Uygulamalı sorular"],
                    "difficulty_levels": ["Kolay: 8 soru", "Orta: 5 soru", "Zor: 2 soru"]
                }}
            ]
        }}
    ],
    "weak_subjects": ["Matematik", "Fizik"],
    "recommendations": [
        "Zayıf konularda günde en az 20 soru çöz",
        "Yanlış yaptığın soruları tekrar et"
    ]
}}

ÖNEMLI FORMAT KURALLARI:
- weak_subjects: Sadece ders isimleri içeren string array olmalı. Örnek: ["Matematik", "Fizik"]
- recommendations: String array olmalı
- daily_plans: Belirtilen yapıda object array olmalı

Yanıtında sadece JSON formatını kullan, başka açıklama ekleme.
"""
        return prompt
    
    def _parse_response(self, response_text: str, student_performance: StudentPerformance) -> StudyPlan:
        """AI yanıtını parse eder ve StudyPlan objesi oluşturur"""
        try:
            # JSON'u extract et (bazen AI extra metin ekliyor)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("Geçerli JSON formatı bulunamadı")
            
            json_str = response_text[start_idx:end_idx]
            parsed_data = json.loads(json_str)
            
            # weak_subjects alanını düzelt (bazen dict listesi geliyor)
            weak_subjects = parsed_data.get("weak_subjects", [])
            if weak_subjects and isinstance(weak_subjects[0], dict):
                # Eğer dict listesi ise, sadece subject isimlerini al
                weak_subjects = [item.get("subject", str(item)) for item in weak_subjects]
            elif not isinstance(weak_subjects, list):
                weak_subjects = []
            
            return StudyPlan(
                student_id=student_performance.student_id,
                student_name=student_performance.name,
                week_number=parsed_data.get("week_number", 1),
                total_questions=parsed_data.get("total_questions", 150),
                daily_plans=parsed_data.get("daily_plans", []),
                weak_subjects=weak_subjects,
                recommendations=parsed_data.get("recommendations", []),
                created_at=datetime.now()
            )
        except json.JSONDecodeError as e:
            raise Exception(f"JSON parse hatası: {e}")
        except Exception as e:
            # Debug için AI yanıtını da ekle
            debug_info = f"AI Yanıtı: {response_text[:500]}..." if len(response_text) > 500 else f"AI Yanıtı: {response_text}"
            raise Exception(f"Yanıt işleme hatası: {e}\n{debug_info}")
