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
log("INFO", "FastAPI Application Starting...")
log("INFO", f"API Key Status: {'✅ LOADED' if WEATHER_API_KEY else '❌ NOT LOADED'}")
if WEATHER_API_KEY:
    log("DEBUG", f"API Key (masked): {WEATHER_API_KEY[:15]}...{'*'*10}")
log("INFO", f"Weather API URL: {WEATHER_API_URL}")
print("="*70 + "\n")

@app.on_event("startup")
async def startup_event():
    log("SUCCESS", "FastAPI server started successfully")
    log("INFO", "Listening on http://127.0.0.1:8000")
    log("INFO", "Webhook endpoint: POST /webhook")

@app.get("/health")
async def health():
    log("INFO", "Health check request received")
    return {"status": "OK", "message": "Weather Bot API is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    """
    Main webhook endpoint that receives requests from Dialogflow
    """
    print("\n" + "🔔"*35)
    log("WEBHOOK", "REQUEST RECEIVED FROM DIALOGFLOW")
    print("🔔"*35 + "\n")
    
    try:
        # Step 1: Get request body
        log("DEBUG", "Step 1: Parsing request body...")
        request_body = await request.json()
        log("SUCCESS", "Request body parsed successfully")
        
        # Step 2: Log full request (pretty print)
        log("DEBUG", "Full request details:")
        print(json.dumps(request_body, indent=2))
        
        # Step 3: Extract parameters
        log("DEBUG", "Step 2: Extracting parameters...")
        query_result = request_body.get('queryResult', {})
        parameters = query_result.get('parameters', {})
        city = parameters.get('city', '')
        date_str = parameters.get('date', None)
        
        log("SUCCESS", "Parameters extracted", f"city='{city}', date='{date_str}'")
        
        # Step 4: Get intent
        log("DEBUG", "Step 3: Identifying intent...")
        intent_name = query_result.get('intent', {}).get('displayName', 'Unknown')
        log("SUCCESS", f"Intent identified: '{intent_name}'")
        
        # Step 5: Validate city
        log("DEBUG", "Step 4: Validating city parameter...")
        if not city or city.strip() == '':
            log("ERROR", "No city provided, using default 'Lahore'")
            city = 'Lahore'
        log("SUCCESS", f"City validated: '{city}'")
        
        # Step 6: Determine action (current weather or forecast)
        log("DEBUG", "Step 5: Determining action type...")
        is_forecast = 'forecast' in intent_name.lower() or bool(date_str)
        action = "FORECAST" if is_forecast else "CURRENT WEATHER"
        log("SUCCESS", f"Action type: {action}")
        
        # Step 7: Call weather API
        log("DEBUG", "Step 6: Calling OpenWeatherMap API...")
        log("API", f"Fetching {action.lower()} for: {city}")
        
        if is_forecast:
            response_text = await get_forecast(city, date_str)
        else:
            response_text = await get_current_weather(city)
        
        # Step 8: Prepare response
        log("DEBUG", "Step 7: Preparing Dialogflow response...")
        dialogflow_response = {
            "fulfillmentText": response_text
        }
        log("SUCCESS", f"Response prepared (length: {len(response_text)} chars)")
        
        # Step 9: Return response
        log("DEBUG", "Step 8: Returning response to Dialogflow...")
        log("SUCCESS", "Webhook request completed successfully!")
        print("\n" + "="*70 + "\n")
        
        return JSONResponse(dialogflow_response)
    
    except Exception as e:
        log("ERROR", f"Exception occurred: {str(e)}")
        import traceback
        log("DEBUG", "Full traceback:")
        print(traceback.format_exc())
        print("\n" + "="*70 + "\n")
        
        return JSONResponse({
            "fulfillmentText": f"Sorry, I encountered an error: {str(e)}"
        }, status_code=200)

async def get_current_weather(city: str) -> str:
    """
    Fetch current weather from OpenWeatherMap API
    """
    print()
    log("DEBUG", f"get_current_weather called", f"city='{city}'")
    
    try:
        url = f"{WEATHER_API_URL}/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        log("API", f"API URL: {url[:70]}...")
        
        log("DEBUG", "Creating httpx AsyncClient...")
        async with httpx.AsyncClient(timeout=10.0) as client:
            log("DEBUG", "Sending GET request to OpenWeatherMap...")
            response = await client.get(url)
            log("API", f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            log("DEBUG", "Parsing JSON response...")
            data = response.json()
            log("SUCCESS", "Weather data retrieved successfully")
            
            # Extract data
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            condition = data['weather'][0]['main']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            pressure = data['main']['pressure']
            
            log("DEBUG", f"Weather data extracted", 
                f"temp={temp}°C, condition={condition}, humidity={humidity}%")
            
            # Format message
            message = f"🌤️ *Current Weather in {city.title()}*\n"
            message += f"━━━━━━━━━━━━━━━━━━━━\n"
            message += f"🌡️ Temperature: {temp}°C\n"
            message += f"🤔 Feels Like: {feels_like}°C\n"
            message += f"☁️ Condition: {condition} ({description})\n"
            message += f"💧 Humidity: {humidity}%\n"
            message += f"💨 Wind Speed: {wind_speed} m/s\n"
            message += f"🔽 Pressure: {pressure} hPa\n"
            message += f"━━━━━━━━━━━━━━━━━━━━"
            
            log("SUCCESS", "Weather message formatted successfully")
            return message
        else:
            error_msg = f"❌ City '{city}' not found (Status: {response.status_code})"
            log("ERROR", error_msg)
            return error_msg
    
    except httpx.TimeoutException:
        error_msg = "❌ Request timeout - API took too long to respond"
        log("ERROR", error_msg)
        return error_msg
    except httpx.RequestError as e:
        error_msg = f"❌ Network error: {str(e)}"
        log("ERROR", error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"❌ Error fetching weather: {str(e)}"
        log("ERROR", error_msg)
        import traceback
        log("DEBUG", "Traceback:", traceback.format_exc())
        return error_msg

async def get_forecast(city: str, date_str: str) -> str:
    """
    Fetch weather forecast from OpenWeatherMap API
    """
    print()
    log("DEBUG", f"get_forecast called", f"city='{city}', date='{date_str}'")
    
    try:
        url = f"{WEATHER_API_URL}/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
        log("API", f"API URL: {url[:70]}...")
        
        log("DEBUG", "Creating httpx AsyncClient...")
        async with httpx.AsyncClient(timeout=10.0) as client:
            log("DEBUG", "Sending GET request to OpenWeatherMap...")
            response = await client.get(url)
            log("API", f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            log("DEBUG", "Parsing JSON response...")
            data = response.json()
            log("SUCCESS", "Forecast data retrieved successfully")
            
            forecast_list = data['list']
            log("DEBUG", f"Got {len(forecast_list)} forecast entries")
            
            # Format message
            message = f"📅 *Weather Forecast for {city.title()}*\n"
            message += f"📊 (Next 8 Days)\n"
            message += f"━━━━━━━━━━━━━━━━━━━━\n\n"
            
            for i in range(0, min(40, len(forecast_list)), 8):
                item = forecast_list[i]
                forecast_date = item['dt_txt'].split()[0]
                temp = item['main']['temp']
                temp_max = item['main']['temp_max']
                temp_min = item['main']['temp_min']
                condition = item['weather'][0]['main']
                humidity = item['main']['humidity']
                
                message += f"📌 *{forecast_date}*\n"
                message += f"   🌡️ Temp: {temp}°C (Min: {temp_min}°C, Max: {temp_max}°C)\n"
                message += f"   ☁️ Condition: {condition}\n"
                message += f"   💧 Humidity: {humidity}%\n"
                message += f"   ─────────────────\n"
            
            log("SUCCESS", "Forecast message formatted successfully")
            return message
        else:
            error_msg = f"❌ Could not fetch forecast for '{city}' (Status: {response.status_code})"
            log("ERROR", error_msg)
            return error_msg
    
    except httpx.TimeoutException:
        error_msg = "❌ Request timeout - API took too long to respond"
        log("ERROR", error_msg)
        return error_msg
    except httpx.RequestError as e:
        error_msg = f"❌ Network error: {str(e)}"
        log("ERROR", error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"❌ Error fetching forecast: {str(e)}"
        log("ERROR", error_msg)
        import traceback
        log("DEBUG", "Traceback:", traceback.format_exc())
        return error_msg

@app.get("/")
async def root():
    log("INFO", "Root endpoint called")
    return {
        "message": "Welcome to Weather Bot API",
        "endpoints": {
            "health": "/health",
            "webhook": "POST /webhook"
        },
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)