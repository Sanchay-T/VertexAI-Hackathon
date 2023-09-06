import requests
from django.conf import settings

class SupabaseService:
    BASE_URL = settings.SUPABASE_URL
    HEADERS = {
        'apikey': settings.SUPABASE_API_KEY,
        'Content-Type': 'application/json'
    }

    @classmethod
    def fetch_data(cls, endpoint):
        response = requests.get(f"{cls.BASE_URL}/{endpoint}", headers=cls.HEADERS)
        return response.json()

    # Add more methods for POST, PUT, DELETE as needed
