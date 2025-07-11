"""
Główny plik aplikacji pogodowej
"""
import tkinter as tk
from weather_gui import WeatherApp  # Import naszej klasy GUI

def main():
    """Funkcja główna aplikacji"""
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()