"""
Moduł GUI dla aplikacji pogodowej
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading

# IMPORT z naszego modułu API
from weather_api import get_weather_data, format_weather_info

class WeatherApp:
    """Klasa odpowiedzialna za interfejs graficzny"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🌤️ Weather App")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        self.create_widgets()
        
    def create_widgets(self):
        """Tworzy wszystkie elementy GUI"""
        # Główny frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tytuł
        title_label = ttk.Label(main_frame, text="🌤️ Weather App", 
                               font=('Arial', 20, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input dla miasta
        ttk.Label(main_frame, text="Podaj miasto:", 
                 font=('Arial', 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.city_entry = ttk.Entry(main_frame, width=30, font=('Arial', 12))
        self.city_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        self.city_entry.bind('<Return>', lambda event: self.get_weather())
        
        # Przycisk
        self.get_weather_btn = ttk.Button(main_frame, text="Pobierz pogodę", 
                                         command=self.get_weather)
        self.get_weather_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Obszar wyników
        self.result_frame = ttk.LabelFrame(main_frame, text="Wyniki", 
                                          padding="15")
        self.result_frame.grid(row=3, column=0, columnspan=2, 
                              sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Text widget z scrollbar
        self.text_widget = tk.Text(self.result_frame, height=15, width=60,
                                  font=('Consolas', 10), wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, 
                                 command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        self.text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Gotowy")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                       pady=(10, 0))
        
        # Konfiguracja grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.rowconfigure(0, weight=1)

    def get_weather(self):
        """Obsługuje kliknięcie przycisku pobierania pogody"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Ostrzeżenie", "Proszę podać nazwę miasta!")
            return
        
        # Uruchom w osobnym wątku żeby nie blokować GUI
        self.get_weather_btn.config(state='disabled')
        self.status_var.set("Pobieranie danych...")
        
        thread = threading.Thread(target=self.fetch_weather_data, args=(city,))
        thread.daemon = True
        thread.start()

    def fetch_weather_data(self, city):
        """Pobiera dane pogodowe w osobnym wątku"""
        try:
            # TUTAJ używamy funkcji z weather_api.py
            weather_data = get_weather_data(city)  # Import z weather_api
            
            if weather_data:
                # TUTAJ też używamy funkcji z weather_api.py
                formatted_result = format_weather_info(weather_data)  # Import z weather_api
                # Aktualizuj GUI w głównym wątku
                self.root.after(0, self.update_results, formatted_result, True)
            else:
                error_msg = f"❌ Nie znaleziono miasta: {city}"
                self.root.after(0, self.update_results, error_msg, False)
                
        except Exception as e:
            error_msg = f"❌ Błąd: {str(e)}"
            self.root.after(0, self.update_results, error_msg, False)

    def update_results(self, result, success):
        """Aktualizuje wyniki w GUI"""
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, result)
        
        if success:
            self.status_var.set("Dane pobrane pomyślnie")
            self.text_widget.config(fg='black')
        else:
            self.status_var.set("Błąd pobierania danych")
            self.text_widget.config(fg='red')
        
        self.get_weather_btn.config(state='normal')