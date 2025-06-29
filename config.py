import os
from dotenv import load_dotenv
from typing import Optional


class Config:
    """Uygulama konfigürasyonu"""
    
    def __init__(self):
        load_dotenv()
        self._gemini_api_key: Optional[str] = None
    
    @property
    def gemini_api_key(self) -> str:
        """Gemini API anahtarını döndürür"""
        if self._gemini_api_key is None:
            self._gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not self._gemini_api_key:
                raise ValueError("GEMINI_API_KEY environment variable is not set")
        return self._gemini_api_key
    
    @property
    def model_name(self) -> str:
        """Kullanılacak model adını döndürür"""
        return "gemini-2.5-flash"
    
    @property
    def max_retries(self) -> int:
        """Maksimum deneme sayısı"""
        return 3
    
    @property
    def timeout(self) -> int:
        """İstek zaman aşımı (saniye)"""
        return 30


# Singleton config instance
config = Config()
