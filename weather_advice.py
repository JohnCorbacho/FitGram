#from dotenv import load_dotenv
#load_dotenv()
import os
import requests
import openai
import streamlit as st
from openai import OpenAI
api_key = os.getenv("WEATHER_API_KEY")

def get_coordinates(city_name, api_key):
    api_key = os.getenv("WEATHER_API_KEY")
    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(geo_url)
    #st.write("Geocoding Response:", response.text)
    data = response.json()
    if data and isinstance(data, list) and len(data) > 0:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    else:
        return None, None


def get_weather_data(city_name, api_key):
    api_key = os.getenv("WEATHER_API_KEY")
    lat, lon = get_coordinates(city_name, api_key)
    if lat is None or lon is None:
        return None

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=imperial&appid={api_key}"
    response = requests.get(weather_url)
    #st.write("Weather API Response:", response.status_code, response.text)
    
    if response.status_code == 200:
        data = response.json()
        current_weather = data.get('weather', [])
        main_data = data.get('main', {})
        weather_description = current_weather[0]['description'] if current_weather else "unknown"
        temp = main_data.get('temp', "unknown")


        return {
            "city": city_name,
            "description": weather_description,
            "temp": temp
        }
    else:
        return None

        

def get_ai_advice(weather):
    client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
    prompt = f"""
    The weather in {weather['city']} is {weather['description']} and {weather['temp']}°F.
    Suggest a very short, motivational workout idea based on that weather. Maximum two lines and use some jokes
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def get_ai_advice_workout(workout):
    client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
    prompt = f"""I want you to act as a personal trainer and give me a workout based on the the muscle that I input. As an example if I ask for Chest you are going to give me excersizes 
    that target that muscle, like Incline chest press, flat bench, High to low cable fly. The muscle is the following:
    {workout}"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
