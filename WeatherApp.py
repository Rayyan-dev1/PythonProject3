"""
🌦 Professional Weather App (Tkinter + OpenWeatherMap API)
Designed to look like a modern mobile weather app.
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

# ---------------- CONFIG ----------------
API_KEY = "361bf9e926b0f29711293965c2e66562"
API_URL = "https://api.openweathermap.org/data/2.5/weather"
APP_BG_PATH = r"C:\Users\Muhammd Reyyan\Desktop\Python\AppBG.jpg"  # ✅ fixed path
# ---------------------------------------


def fetch_weather(city: str):
    """Fetch weather data from API"""
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "en"}
        resp = requests.get(API_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("cod") != 200:
            return None, data.get("message", "Error occurred")

        return data, None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def show_weather():
    """Get city input and display weather"""
    city = city_entry.get().strip()
    if not city or city == "🔍 Enter city name":
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    data, error = fetch_weather(city)
    if error:
        messagebox.showerror("Error", f"Could not fetch weather:\n{error}")
        return

    # Extract info
    name = data.get("name", "Unknown city")
    country = data.get("sys", {}).get("country", "")
    main = data.get("main", {})
    wind = data.get("wind", {})
    weather_list = data.get("weather", [])
    desc = weather_list[0].get("description", "").capitalize() if weather_list else ""

    temp = main.get("temp")
    feels = main.get("feels_like")
    humidity = main.get("humidity")
    wind_speed = wind.get("speed")

    # Clear previous results
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Big temp + city
    tk.Label(result_frame, text=f"{temp}°C", font=("Segoe UI", 42, "bold"),
             bg="#121212", fg="white").pack(pady=(10, 0))

    tk.Label(result_frame, text=f"{name}, {country}",
             font=("Segoe UI", 18, "bold"), bg="#121212", fg="#90caf9").pack(pady=5)

    tk.Label(result_frame, text=desc, font=("Segoe UI", 16, "italic"),
             bg="#121212", fg="white").pack(pady=(0, 15))

    # Extra details grid
    detail_frame = tk.Frame(result_frame, bg="#1E1E1E")
    detail_frame.pack(pady=10, fill="x", padx=15)

    def add_detail(row, col, emoji, label, value):
        box = tk.Frame(detail_frame, bg="#1E1E1E", padx=10, pady=10)
        box.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        tk.Label(box, text=emoji, font=("Segoe UI Emoji", 20),
                 bg="#1E1E1E", fg="white").pack()
        tk.Label(box, text=label, font=("Segoe UI", 12, "bold"),
                 bg="#1E1E1E", fg="#90caf9").pack(pady=(2, 0))
        tk.Label(box, text=value, font=("Segoe UI", 12),
                 bg="#1E1E1E", fg="white").pack()

    add_detail(0, 0, "🌡", "Feels Like", f"{feels}°C")
    add_detail(0, 1, "💧", "Humidity", f"{humidity}%")
    add_detail(0, 2, "💨", "Wind", f"{wind_speed} m/s")


# ---------------- CUSTOM WIDGETS ----------------
class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=350, height=55,
                 bg1="#004b88", bg2="#002648", fg="white", radius=0, **kwargs):
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, bg=parent["bg"], **kwargs)
        self.command = command
        self.bg1, self.bg2, self.fg_color, self.radius = bg1, bg2, fg, radius
        self.width, self.height = width, height

        # Draw gradient-like effect with two rect layers
        self.rect1 = self.create_rounded_rect(0, 0, width, height, radius, fill=self.bg1)
        self.rect2 = self.create_rounded_rect(0, 0, width, height, radius, fill=self.bg2, stipple="gray25")
        self.text_item = self.create_text(width//2, height//2, text=text,
                                          fill=self.fg_color, font=("Segoe UI", 13, "bold"))

        # Bind actions
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def create_rounded_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        points = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y2-r,
                  x2, y2, x2-r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y1+r, x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event): 
        if self.command: self.command()

    def on_enter(self, event): 
        self.itemconfig(self.rect1, fill="#64b5f6")

    def on_leave(self, event): 
        self.itemconfig(self.rect1, fill=self.bg1)


# ---------------- MAIN APP ----------------
root = tk.Tk()
root.geometry("500x700")
root.resizable(False, False)
root.title("Weather App")

# Background
bg_image = Image.open(APP_BG_PATH).resize((500, 700))
bg_photo = ImageTk.PhotoImage(bg_image)
tk.Label(root, image=bg_photo).place(x=0, y=0, relwidth=1, relheight=1)

# ---- Title Bar ----
title_label = tk.Label(root, text="🌦 Weather Now", font=("Segoe UI", 20, "bold"),
                       bg="#0d47a1", fg="white", pady=14)
title_label.pack(fill="x")

# ---- Search Box ----
def on_entry_click(event):
    if city_entry.get() == "🔍 Enter city name":
        city_entry.delete(0, "end")
        city_entry.config(fg="white")

def on_focusout(event):
    if city_entry.get() == "":
        city_entry.insert(0, "🔍 Enter city name")
        city_entry.config(fg="grey")

search_frame = tk.Frame(root, bg="#121212")
search_frame.pack(pady=20)

city_entry = tk.Entry(search_frame, font=("Segoe UI", 14), justify="center",
                      relief="flat", bd=5, fg="grey", bg="#1E1E1E",
                      insertbackground="white", width=20)
city_entry.insert(0, "🔍 Enter city name")
city_entry.bind("<FocusIn>", on_entry_click)
city_entry.bind("<FocusOut>", on_focusout)
city_entry.pack(ipady=10, padx=20)

# ---- Search Button ----
search_button = ModernButton(root, text="Get Weather", command=show_weather)
search_button.pack(pady=20)

# ---- Weather Result Card ----
result_frame = tk.Frame(root, bg="#131313", bd=0, highlightthickness=0)
result_frame.pack(pady=25, expand=True, padx=20)

# ---- Footer ----
footer_label = tk.Label(root, text="Designed and Developed by Rayyan",
                        font=("Segoe UI", 10, "italic"), bg="black", fg="white", pady=6)
footer_label.pack(side="bottom", fill="x")

root.mainloop()
