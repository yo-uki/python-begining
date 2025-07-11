"""
Moduł do pobierania danych pogodowych z API
"""
import requests
from typing import Optional, Dict

API_KEY = "c18a4a1495e30c11dc19028ecbdb5efa"

def get_weather_data(miasto: str) -> Optional[Dict]:
    """
    Pobiera dane pogodowe dla danego miasta
    
    Args:
        miasto: Nazwa miasta
        
    Returns:
        Słownik z danymi pogodowymi lub None jeśli błąd
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={miasto}&appid={API_KEY}&units=metric&lang=pl"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Błąd pobierania danych: {e}")
        return None

def format_weather_info(data: Dict) -> str:
    """
    Formatuje dane pogodowe do czytelnego formatu
    
    Args:
        data: Słownik z danymi pogodowymi
        
    Returns:
        Sformatowany string z informacjami o pogodzie
    """
    if not data:
        return "Nie udało się pobrać danych pogodowych"
    
    miasto = data["name"]
    kraj = data["sys"]["country"]
    temp = data["main"]["temp"]
    temp_odczuwalna = data["main"]["feels_like"]
    wilgotnosc = data["main"]["humidity"]
    cisnienie = data["main"]["pressure"]
    opis = data["weather"][0]["description"].capitalize()
    
    return f"""🌤️  POGODA W {miasto.upper()}, {kraj}
{'='*50}

🌡️  Temperatura: {temp}°C 
    (odczuwalna: {temp_odczuwalna}°C)

📝 Opis: {opis}

💧 Wilgotność: {wilgotnosc}%

🔽 Ciśnienie: {cisnienie} hPa

{'='*50}
Pobrano: {data.get('dt', 'brak danych')}
"""