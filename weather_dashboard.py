#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌤️ Weather Dashboard - داشبورد آب و هوا
استفاده از OpenWeatherMap API
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, Optional, List
import time

class WeatherDashboard:
    """داشبورد آب و هوا با ویژگی‌های پیشرفته"""
    
    def __init__(self, api_key: str = "demo"):
        """
        سازنده Dashboard
        
        Args:
            api_key: کلید API OpenWeatherMap
            برای کلید رایگان از https://openweathermap.org/api ثبت‌نام کنید
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cities_data = {}
        self.cache = {}
        self.cache_time = 600  # 10 دقیقه
        
    def get_current_weather(self, city: str, units: str = "metric") -> Optional[Dict]:
        """
        دریافت آب و هوای فعلی یک شهر
        
        Args:
            city: نام شهر
            units: واحد دما (metric=C, imperial=F)
            
        Returns:
            دیکشنری با اطلاعات آب و هوا یا None
        """
        # بررسی cache
        cache_key = f"{city}_{units}"
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if time.time() - cached_time < self.cache_time:
                return cached_data
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # ذخیره در cache
            self.cache[cache_key] = (time.time(), data)
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ خطا در دریافت اطلاعات: {e}")
            return None
    
    def get_forecast(self, city: str, units: str = "metric") -> Optional[List[Dict]]:
        """
        دریافت پیش‌بینی 5 روزه
        
        Args:
            city: نام شهر
            units: واحد دما
            
        Returns:
            لیست پیش‌بینی‌ها
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("list", [])
            
        except requests.exceptions.RequestException as e:
            print(f"❌ خطا در دریافت پیش‌بینی: {e}")
            return None
    
    def get_air_quality(self, lat: float, lon: float) -> Optional[Dict]:
        """
        دریافت کیفیت هوا بر اساس مختصات
        
        Args:
            lat: عرض جغرافیایی
            lon: طول جغرافیایی
            
        Returns:
            دیکشنری با اطلاعات کیفیت هوا
        """
        try:
            url = "https://api.openweathermap.org/data/3.0/stations"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  خطا در دریافت کیفیت هوا: {e}")
            return None
    
    def display_weather(self, city: str, units: str = "metric"):
        """
        نمایش اطلاعات آب و هوا به صورت گرافیکی
        
        Args:
            city: نام شهر
            units: واحد دما
        """
        weather = self.get_current_weather(city, units)
        
        if not weather:
            print(f"❌ نتوانستم اطلاعات {city} را دریافت کنم")
            return
        
        # استخراج اطلاعات
        temp = weather["main"]["temp"]
        feels_like = weather["main"]["feels_like"]
        humidity = weather["main"]["humidity"]
        pressure = weather["main"]["pressure"]
        wind_speed = weather["wind"]["speed"]
        description = weather["weather"][0]["description"]
        icon = weather["weather"][0]["main"]
        
        unit_symbol = "°C" if units == "metric" else "°F"
        
        # نمایش
        print("\n" + "=" * 60)
        print(f"🌍 {weather['name']}, {weather['sys']['country']}")
        print("=" * 60)
        print()
        
        # نماد آب و هوا
        icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Snow": "❄️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Mist": "🌫️",
            "Smoke": "💨",
            "Haze": "🌫️",
            "Dust": "💨",
            "Fog": "🌫️",
            "Sand": "💨",
            "Ash": "💨",
            "Squall": "💨",
            "Tornado": "🌪️"
        }
        
        weather_icon = icons.get(icon, "🌤️")
        
        print(f"  {weather_icon} {description.title()}")
        print()
        
        # دما
        print(f"  🌡️  دمای فعلی:      {temp}{unit_symbol}")
        print(f"  🤔 احساس دما:       {feels_like}{unit_symbol}")
        print(f"  💧 رطوبت:          {humidity}%")
        print(f"  🔽 فشار:           {pressure} hPa")
        print(f"  💨 سرعت باد:        {wind_speed} m/s")
        
        # شروق و غروب آفتاب
        sunrise = datetime.fromtimestamp(weather["sys"]["sunrise"])
        sunset = datetime.fromtimestamp(weather["sys"]["sunset"])
        
        print()
        print(f"  🌅 شروق آفتاب:      {sunrise.strftime('%H:%M:%S')}")
        print(f"  🌇 غروب آفتاب:      {sunset.strftime('%H:%M:%S')}")
        
        print()
        print("=" * 60)
    
    def display_forecast(self, city: str, days: int = 5, units: str = "metric"):
        """
        نمایش پیش‌بینی آب و هوا
        
        Args:
            city: نام شهر
            days: تعداد روزها
            units: واحد دما
        """
        forecast_data = self.get_forecast(city, units)
        
        if not forecast_data:
            print(f"❌ نتوانستم پیش‌بینی {city} را دریافت کنم")
            return
        
        unit_symbol = "°C" if units == "metric" else "°F"
        
        print("\n" + "=" * 80)
        print(f"📅 پیش‌بینی آب و هوای {city}")
        print("=" * 80)
        print()
        
        # گروه‌بندی بر اساس روز
        daily_data = {}
        for item in forecast_data:
            date = datetime.fromtimestamp(item["dt"]).date()
            if date not in daily_data:
                daily_data[date] = []
            daily_data[date].append(item)
        
        # نمایش
        icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Snow": "❄️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Mist": "🌫️",
        }
        
        count = 0
        for date, items in list(daily_data.items())[:days]:
            if count >= days:
                break
            count += 1
            
            # میانگین‌های روزانه
            temps = [item["main"]["temp"] for item in items]
            descriptions = [item["weather"][0]["main"] for item in items]
            
            avg_temp = sum(temps) / len(temps)
            min_temp = min(temps)
            max_temp = max(temps)
            
            # نماد غالب
            main_icon = max(set(descriptions), key=descriptions.count)
            icon = icons.get(main_icon, "🌤️")
            
            print(f"{date} {icon}")
            print(f"  🌡️  میانگین: {avg_temp:.1f}{unit_symbol}")
            print(f"  ❄️  حداقل:  {min_temp:.1f}{unit_symbol}")
            print(f"  🔥 حداکثر:  {max_temp:.1f}{unit_symbol}")
            print()
        
        print("=" * 80)
    
    def compare_cities(self, cities: List[str], units: str = "metric"):
        """
        مقایسه آب و هوای چند شهر
        
        Args:
            cities: لیست شهرها
            units: واحد دما
        """
        print("\n" + "=" * 100)
        print("🌍 مقایسه آب و هوای شهرها")
        print("=" * 100)
        print()
        
        # عنوان
        print(f"{'شهر':<20} {'دما':<15} {'احساس':<15} {'رطوبت':<15} {'باد':<15} {'وضعیت':<20}")
        print("-" * 100)
        
        unit_symbol = "°C" if units == "metric" else "°F"
        
        for city in cities:
            weather = self.get_current_weather(city, units)
            
            if weather:
                name = weather["name"]
                temp = f"{weather['main']['temp']:.1f}{unit_symbol}"
                feels = f"{weather['main']['feels_like']:.1f}{unit_symbol}"
                humidity = f"{weather['main']['humidity']}%"
                wind = f"{weather['wind']['speed']:.1f} m/s"
                description = weather["weather"][0]["description"]
                
                print(f"{name:<20} {temp:<15} {feels:<15} {humidity:<15} {wind:<15} {description:<20}")
            else:
                print(f"{city:<20} {'❌ خطا':<15}")
        
        print()
        print("=" * 100)
    
    def save_weather_data(self, cities: List[str], filename: str = "weather_data.json"):
        """
        ذخیره اطلاعات آب و هوا در فایل
        
        Args:
            cities: لیست شهرها
            filename: نام فایل
        """
        data = {}
        
        for city in cities:
            weather = self.get_current_weather(city)
            if weather:
                data[city] = {
                    "temperature": weather["main"]["temp"],
                    "feels_like": weather["main"]["feels_like"],
                    "humidity": weather["main"]["humidity"],
                    "pressure": weather["main"]["pressure"],
                    "wind_speed": weather["wind"]["speed"],
                    "description": weather["weather"][0]["description"],
                    "timestamp": datetime.now().isoformat()
                }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ اطلاعات در {filename} ذخیره شدند")
    
    def interactive_mode(self):
        """
        حالت تعاملی داشبورد
        """
        print("\n" + "=" * 60)
        print("🌤️  Weather Dashboard - حالت تعاملی")
        print("=" * 60)
        print()
        print("دستورات:")
        print("  1. شهر - نمایش آب و هوای یک شهر")
        print("  2. پیش‌بینی [شهر] - نمایش پیش‌بینی 5 روزه")
        print("  3. مقایسه - مقایسه آب و هوای چند شهر")
        print("  4. ذخیره - ذخیره اطلاعات")
        print("  5. خروج - خروج از برنامه")
        print()
        
        while True:
            try:
                command = input("🎯 دستور خود را وارد کنید: ").strip()
                
                if command == "خروج" or command == "5":
                    print("👋 خداحافظ!")
                    break
                
                elif command.startswith("1") or command.startswith("شهر"):
                    city = input("🏙️  نام شهر را وارد کنید: ").strip()
                    if city:
                        self.display_weather(city)
                
                elif command.startswith("2") or command.startswith("پیش‌بینی"):
                    city = input("🏙️  نام شهر را وارد کنید: ").strip()
                    if city:
                        self.display_forecast(city)
                
                elif command.startswith("3") or command.startswith("مقایسه"):
                    cities_input = input("🌍 شهرها را با کاما جدا کنید: ").strip()
                    cities = [c.strip() for c in cities_input.split(",")]
                    if cities:
                        self.compare_cities(cities)
                
                elif command.startswith("4") or command.startswith("ذخیره"):
                    cities_input = input("🌍 شهرها را با کاما جدا کنید: ").strip()
                    cities = [c.strip() for c in cities_input.split(",")]
                    if cities:
                        filename = input("📄 نام فایل (پیش‌فرض: weather_data.json): ").strip()
                        if not filename:
                            filename = "weather_data.json"
                        self.save_weather_data(cities, filename)
                
                else:
                    print("❌ دستور نامشخص است")
                
            except KeyboardInterrupt:
                print("\n👋 خداحافظ!")
                break
            except Exception as e:
                print(f"❌ خطا: {e}")


def main():
    """تابع اصلی"""
    
    # کلید API - از https://openweathermap.org/api ثبت‌نام کنید
    # API_KEY = "YOUR_API_KEY_HERE"
    # برای تست از کلید Demo استفاده می‌کنیم
    API_KEY = "demo"
    
    # اگر کلید واقعی دارید:
    # API_KEY = os.environ.get("OPENWEATHER_API_KEY", "demo")
    
    dashboard = WeatherDashboard(api_key=API_KEY)
    
    # نمونه استفاده
    print("=" * 60)
    print("🌤️  Weather Dashboard Demo")
    print("=" * 60)
    print()
    
    # نمایش آب و هوای چند شهر
    cities = ["Tehran", "London", "New York", "Tokyo"]
    
    print("📡 دریافت اطلاعات آب و هوا...")
    print()
    
    for city in cities:
        dashboard.display_weather(city)
    
    # مقایسه
    dashboard.compare_cities(cities)
    
    # حالت تعاملی
    dashboard.interactive_mode()


if __name__ == "__main__":
    main()
