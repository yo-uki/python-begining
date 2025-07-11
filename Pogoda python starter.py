import requests
from functools import partial, reduce
from typing import Optional, Dict, List

API_KEY = "c18a4a1495e30c11dc19028ecbdb5efa"

# Pure functions - bez efektów ubocznych
def create_url(miasto: str, api_key: str) -> str:
    """Tworzy URL dla API - pure function"""
    return f"https://api.openweathermap.org/data/2.5/weather?q={miasto}&appid={api_key}&units=metric&lang=pl"

def fetch_data(url: str) -> Optional[Dict]:
    """Pobiera dane z URL - jedyny efekt uboczny to HTTP request"""
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def extract_weather_info(data: Dict) -> Dict:
    """Wyciąga potrzebne informacje - pure function"""
    if not data:
        return {}
    
    return {
        'miasto': data["name"],
        'kraj': data["sys"]["country"],
        'temp': data["main"]["temp"],
        'temp_odczuwalna': data["main"]["feels_like"],
        'wilgotnosc': data["main"]["humidity"],
        'cisnienie': data["main"]["pressure"],
        'opis': data["weather"][0]["description"].capitalize()
    }

def format_weather_display(weather_info: Dict) -> str:
    """Formatuje dane do wyświetlenia - pure function"""
    if not weather_info:
        return "Nie udało się pobrać danych pogodowych"
    
    return f"""
{'='*50}
🌤️  POGODA W {weather_info['miasto'].upper()}, {weather_info['kraj']}
{'='*50}
🌡️  Temperatura: {weather_info['temp']}°C (odczuwalna: {weather_info['temp_odczuwalna']}°C)
📝 Opis: {weather_info['opis']}
💧 Wilgotność: {weather_info['wilgotnosc']}%
🔽 Ciśnienie: {weather_info['cisnienie']} hPa
{'='*50}
"""

# Funkcje wyższego rzędu i kompozycja
def compose(*functions):
    """Komponuje funkcje - klasyk programowania funkcyjnego"""
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def pipe(value, *functions):
    """Pipeline - przepuszcza wartość przez funkcje"""
    return reduce(lambda acc, func: func(acc), functions, value)

# Partial application - currying
def create_weather_pipeline(api_key: str):
    """Tworzy pipeline dla danego API key"""
    url_creator = partial(create_url, api_key=api_key)
    
    def get_weather_for_city(miasto: str) -> str:
        return pipe(
            miasto,
            url_creator,
            fetch_data,
            extract_weather_info,
            format_weather_display
        )
    
    return get_weather_for_city

# Map/Filter/Reduce - klasyczne funkcje funkcyjne
def get_weather_for_multiple_cities(miasta: List[str], api_key: str) -> List[str]:
    """Pobiera pogodę dla wielu miast naraz"""
    weather_getter = create_weather_pipeline(api_key)
    return list(map(weather_getter, miasta))

def filter_valid_weather(weather_results: List[str]) -> List[str]:
    """Filtruje tylko poprawne wyniki"""
    return list(filter(lambda result: "Nie udało się" not in result, weather_results))

# Efekty uboczne (I/O) oddzielone na końcu
def main_functional():
    """Główna funkcja z minimalnym I/O"""
    print("Podaj miasta oddzielone przecinkami:")
    input_cities = input().split(',')
    miasta = [miasto.strip() for miasto in input_cities if miasto.strip()]
    
    # Funkcyjny pipeline
    weather_results = get_weather_for_multiple_cities(miasta, API_KEY)
    valid_results = filter_valid_weather(weather_results)
    
    # Wyświetlenie (jedyny efekt uboczny)
    for result in valid_results:
        print(result)

if __name__ == "__main__":
    main_functional()