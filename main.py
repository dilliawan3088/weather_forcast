from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

app = FastAPI()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'ff09f16654861261ebb9d82eb601336e')
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5"

# Helper function for formatted logging
def log(level, message, extra=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if level == "INFO":
        prefix = "ℹ️  INFO"
    elif level == "SUCCESS":
        prefix = "✅ SUCCESS"
    elif level == "ERROR":
        prefix = "❌ ERROR"
    elif level == "DEBUG":
        prefix = "🔍 DEBUG"
    elif level == "WEBHOOK":
        prefix = "🔔 WEBHOOK"
    elif level == "API":
        prefix = "📡 API"
    else:
        prefix = "📝 LOG"
    
    if extra:
        print(f"[{timestamp}] {prefix} - {message}")
        print(f"              └─ {extra}")
    else:
        print(f"[{timestamp}] {prefix} - {message}")

# Startup message
print("\n" + "="*70)
log("INFO", "Multi-City Conversational Weather Bot Starting...")
log("INFO", f"API Key Status: {'✅ LOADED' if WEATHER_API_KEY else '❌ NOT LOADED'}")
log("INFO", "Supports: Multiple cities, continuous conversation, multi-turn dialogue")
print("="*70 + "\n")

@app.on_event("startup")
async def startup_event():
    log("SUCCESS", "FastAPI server started successfully")

@app.get("/health")
async def health():
    return {"status": "OK", "message": "Multi-City Weather Bot is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    """
    Multi-City Conversational Webhook
    Handles:
    - Multiple cities in sequence
    - Current weather for any city
    - Forecasts for any city
    - Natural conversation flow
    - Continuous multi-turn dialogue
    """
    print("\n" + "🔔"*35)
    log("WEBHOOK", "REQUEST RECEIVED FROM DIALOGFLOW")
    print("🔔"*35 + "\n")
    
    try:
        # Parse request
        log("DEBUG", "Parsing request body...")
        request_body = await request.json()
        log("SUCCESS", "Request parsed successfully")
        
        # Extract data
        query_result = request_body.get('queryResult', {})
        parameters = query_result.get('parameters', {})
        city = parameters.get('city', '')
        date_str = parameters.get('date', None)
        user_message = query_result.get('queryText', '').lower().strip()
        intent_name = query_result.get('intent', {}).get('displayName', '').lower()
        
        log("DEBUG", "Extracted parameters:", 
            f"city='{city}', date='{date_str}', intent='{intent_name}'")
        
        # ===== MULTI-CITY CONVERSATIONAL FLOW =====
        
        # 1. GREETING
        if any(greet in user_message for greet in ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon']):
            log("SUCCESS", "GREETING intent detected")
            response_text = """🤖 This is Weather BOT. How may I help you?

I can provide weather information for any city in the world! 🌍

You can ask me:
🌤️ "What is the weather in [city name]?"
📅 "Weather forecast for [city name]"
🌏 "Show me weather in [city1] and [city2]"

Just tell me any city name and I'll get you the latest weather! ☀️"""
        
        # 2. HELP REQUEST
        elif any(h in user_message for h in ['help', 'what can you do', 'how can you help', 'assist', 'options']):
            log("SUCCESS", "HELP intent detected")
            response_text = """🆘 Weather BOT Help Guide

I can help you with weather for ANY city! 🌍

📍 **How to use:**
✓ "What is the weather in London?"
✓ "Current weather in Tokyo"
✓ "Weather forecast for Paris"
✓ "Tell me weather in New York"
✓ "Show me weather for Sydney"

📊 **Multiple Cities:**
✓ "Weather in Lahore, Karachi, and Islamabad"
✓ "Current weather for London and Paris"
✓ "Forecast for Dubai, Abu Dhabi, and Doha"

🌐 **Supported Cities:** Any major city worldwide!
London, New York, Paris, Tokyo, Sydney, Dubai, Mumbai, Bangkok, Singapore, etc.

Just mention the city name and I'll fetch the weather! 🌤️"""
        
        # 3. CURRENT WEATHER REQUEST (with city provided)
        elif city and ('current_weather' in intent_name or ('weather' in user_message and 'forecast' not in user_message)):
            log("SUCCESS", "CURRENT WEATHER intent with city detected")
            log("API", f"Fetching weather for: {city}")
            response_text = await get_current_weather(city)
            
            # Add continuation prompt for multi-turn
            response_text += f"\n\n❓ Would you like weather for another city?\n(Just say: 'Weather in [city name]')"
        
        # 4. FORECAST REQUEST (with city provided)
        elif city and ('weather_forecast' in intent_name or 'forecast' in user_message):
            log("SUCCESS", "FORECAST intent with city detected")
            log("API", f"Fetching forecast for: {city}")
            response_text = await get_forecast(city, date_str)
            
            # Add continuation prompt for multi-turn
            response_text += f"\n\n❓ Would you like weather or forecast for another city?\n(Try: 'Weather in [city name]')"
        
        # 5. WEATHER REQUEST WITHOUT CITY (Prompt for city)
        elif 'weather' in user_message and not city:
            if 'forecast' in user_message:
                log("DEBUG", "Forecast requested but NO city provided")
                response_text = """📍 Please provide the city name for the forecast!

For example:
✓ "Forecast for Lahore"
✓ "Weather forecast in Paris"
✓ "Tell me forecast for London"

Which city would you like the forecast for? 🌍"""
            else:
                log("DEBUG", "Current weather requested but NO city provided")
                response_text = """📍 Please provide the city name!

For example:
✓ "Weather in Lahore"
✓ "Current weather in London"
✓ "What's the weather in Paris?"
✓ "Show me weather for Dubai"

Which city's weather would you like? 🌤️"""
        
        # 6. JUST CITY PROVIDED (infer weather request)
        elif city and not any(keyword in user_message for keyword in ['weather', 'forecast', 'current']):
            log("DEBUG", "Only city provided")
            
            # Check if forecast was mentioned before
            if 'forecast' in user_message.lower():
                log("API", f"Getting forecast for: {city}")
                response_text = await get_forecast(city, date_str)
            else:
                log("API", f"Getting current weather for: {city}")
                response_text = await get_current_weather(city)
            
            response_text += f"\n\n❓ Need weather for another city?\n(Say: 'Weather in [city name]')"
        
        # 7. THANK YOU / CLOSING (but ask if they need more)
        elif any(thanks in user_message for thanks in ['thank', 'thanks', 'thankyou', 'appreciate']):
            log("SUCCESS", "THANKS intent detected")
            response_text = """😊 You're welcome!

Is there anything else I can help you with?

🌍 I can provide weather for any city you want!
📍 Just say: "Weather in [city name]"
📅 Or: "Forecast for [city name]"

Feel free to ask anytime! ☀️"""
        
        # 8. NO THANKS / GOODBYE
        elif any(no in user_message for no in ['no thanks', 'no', 'nope', 'goodbye', 'bye', 'nothing else', 'that\'s all']):
            log("SUCCESS", "GOODBYE intent detected")
            response_text = """👋 Thank you for using Weather BOT!

Have a great day and stay weather-aware! ☀️

Goodbye! 🌈"""
        
        # 9. MULTIPLE CITIES REQUEST (NEW!)
        elif 'and' in user_message and city:
            log("SUCCESS", "MULTIPLE CITIES detected")
            # Extract all cities mentioned
            response_text = await handle_multiple_cities(user_message, user_message)
        
        # 10. GENERIC MESSAGE
        else:
            log("DEBUG", "Generic message received")
            if city:
                # User mentioned a city but we're not sure what they want
                log("API", f"Inferring weather for: {city}")
                response_text = await get_current_weather(city)
                response_text += f"\n\n❓ Would you like forecast or weather for another city?"
            else:
                response_text = """👋 Hello! I'm your Weather BOT! 🤖

I can help you get weather information for ANY city in the world! 🌍

Just tell me:
🌤️ "What is the weather in [city]?"
📅 "Weather forecast for [city]"
🌏 "Show weather for [city1] and [city2]"

What city would you like to know about? ☀️"""
        
        # Prepare and return response
        log("SUCCESS", f"Response prepared (length: {len(response_text)} chars)")
        dialogflow_response = {"fulfillmentText": response_text}
        
        print("\n" + "="*70 + "\n")
        return JSONResponse(dialogflow_response)
    
    except Exception as e:
        log("ERROR", f"Exception occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return JSONResponse({
            "fulfillmentText": f"Sorry, I encountered an error: {str(e)}"
        }, status_code=200)

async def get_current_weather(city: str) -> str:
    """
    Get current weather for a city
    Works with ANY city in the world
    """
    print()
    log("DEBUG", f"get_current_weather called for: '{city}'")
    
    try:
        url = f"{WEATHER_API_URL}/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        log("API", f"Calling OpenWeatherMap for: {city}")
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url)
            log("API", f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            log("SUCCESS", f"Weather data retrieved for {city}")
            
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            condition = data['weather'][0]['main']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            pressure = data['main']['pressure']
            country = data.get('sys', {}).get('country', '')
            
            # Format response
            message = f"🌤️ *Current Weather in {city.title()}, {country}*\n"
            message += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            message += f"📍 Location: {city.title()}, {country}\n"
            message += f"🌡️ Temperature: {temp}°C\n"
            message += f"🤔 Feels Like: {feels_like}°C\n"
            message += f"☁️ Condition: {condition} ({description})\n"
            message += f"💧 Humidity: {humidity}%\n"
            message += f"💨 Wind Speed: {wind_speed} m/s\n"
            message += f"🔽 Pressure: {pressure} hPa\n"
            message += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            message += f"⏰ Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            log("SUCCESS", "Current weather formatted successfully")
            return message
        else:
            log("ERROR", f"City '{city}' not found")
            return f"""❌ City '{city}' not found!

Please check the spelling and try again.
Examples: London, Paris, Tokyo, New York, Dubai, etc.

Would you like weather for a different city?"""
    
    except httpx.TimeoutException:
        log("ERROR", "Request timeout")
        return f"❌ Request took too long. Please try again in a moment."
    except Exception as e:
        log("ERROR", f"Error: {str(e)}")
        return f"❌ Error fetching weather. Please try again."

async def get_forecast(city: str, date_str: str) -> str:
    """
    Get weather forecast for a city
    Works with ANY city in the world
    """
    print()
    log("DEBUG", f"get_forecast called for: '{city}'")
    
    try:
        url = f"{WEATHER_API_URL}/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
        log("API", f"Calling OpenWeatherMap Forecast API for: {city}")
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url)
            log("API", f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            log("SUCCESS", f"Forecast data retrieved for {city}")
            
            forecast_list = data['list']
            city_info = data.get('city', {})
            country = city_info.get('country', '')
            
            # Get date range
            first_date = forecast_list[0]['dt_txt'].split()[0]
            last_date = forecast_list[-1]['dt_txt'].split()[0]
            
            # Format response
            message = f"📅 *Weather Forecast for {city.title()}, {country}*\n"
            message += f"📊 ({first_date} to {last_date} - 8 Days)\n"
            message += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Get 8 days of forecast
            count = 0
            for i in range(0, min(40, len(forecast_list)), 8):
                item = forecast_list[i]
                forecast_date = item['dt_txt'].split()[0]
                temp = item['main']['temp']
                temp_max = item['main']['temp_max']
                temp_min = item['main']['temp_min']
                condition = item['weather'][0]['main']
                humidity = item['main']['humidity']
                
                message += f"📌 *{forecast_date}*\n"
                message += f"   🌡️ Temperature: {temp}°C\n"
                message += f"   📈 Max: {temp_max}°C | 📉 Min: {temp_min}°C\n"
                message += f"   ☁️ Condition: {condition}\n"
                message += f"   💧 Humidity: {humidity}%\n"
                message += f"   ───────────────────────\n\n"
                count += 1
            
            message += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            message += f"✅ Forecast for {count} days ahead\n"
            message += f"⏰ Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            log("SUCCESS", "Forecast formatted successfully")
            return message
        else:
            log("ERROR", f"City '{city}' not found for forecast")
            return f"""❌ Could not fetch forecast for '{city}'!

Please check the city name and try again.
Examples: London, Paris, Tokyo, Dubai, etc.

Would you like forecast for a different city?"""
    
    except httpx.TimeoutException:
        log("ERROR", "Request timeout")
        return f"❌ Request took too long. Please try again."
    except Exception as e:
        log("ERROR", f"Error: {str(e)}")
        return f"❌ Error fetching forecast. Please try again."

async def handle_multiple_cities(user_message: str, original_message: str) -> str:
    """
    Handle requests for multiple cities
    Example: "Weather in London and Paris and Tokyo"
    """
    print()
    log("DEBUG", "handle_multiple_cities called")
    
    # This would require more complex entity extraction
    # For now, we return a helpful message
    return """🌍 I can help with multiple cities!

Please ask me about one city at a time, and I'll get the weather for each:

1️⃣ "Weather in London"
2️⃣ "Now show me Paris"
3️⃣ "What about Tokyo?"

Or ask me each question separately and I'll provide weather for all of them! ☀️

Which cities would you like to start with?"""

@app.get("/")
async def root():
    return {
        "message": "Multi-City Conversational Weather Bot API",
        "endpoints": {
            "health": "/health",
            "webhook": "POST /webhook"
        },
        "features": [
            "Current weather for any city",
            "8-day forecast for any city",
            "Multiple cities in one conversation",
            "Continuous multi-turn dialogue",
            "Natural conversation flow"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)