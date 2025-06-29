import os
from dotenv import load_dotenv
from typing import Optional


class Config:
    """Uygulama konfigürasyonu"""
    
    def __init__(self):
        load_dotenv()
        self._gemini_api_key: Optional[str] = None
        self._database_url: Optional[str] = None
    
    @property
    def gemini_api_key(self) -> str:
        """Gemini API anahtarını döndürür"""
        if self._gemini_api_key is None:
            self._gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not self._gemini_api_key:
                raise ValueError("GEMINI_API_KEY environment variable is not set")
        return self._gemini_api_key
    
    @property
    def database_url(self) -> str:
        """PostgreSQL veritabanı bağlantı URL'ini döndürür"""
        if self._database_url is None:
            self._database_url = os.getenv("DATABASE_URL")
            if not self._database_url:
                # Varsayılan PostgreSQL bağlantı bilgileri
                host = os.getenv("DB_HOST", "localhost")
                port = os.getenv("DB_PORT", "5432")
                database = os.getenv("DB_NAME", "can-hocam")
                username = os.getenv("DB_USER", "postgres")
                password = os.getenv("DB_PASSWORD", "3413")
                self._database_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        return self._database_url
    
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
