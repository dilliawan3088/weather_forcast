# FastAPI + Dialogflow Integration Guide

## Architecture Overview

```
┌─────────────────┐
│     User        │
│ "What's the     │
│  weather?"      │
└────────┬────────┘
         │
         ▼
┌──────────────────┐
│   Dialogflow     │ (Google Cloud)
│   ├─ Intents     │
│   └─ Entities    │
└────────┬─────────┘
         │ Sends JSON to webhook
         ▼
    ┌────────────────────────┐
    │  Your FastAPI Server   │
    │  (main.py)             │
    │  ├─ POST /webhook      │
    │  └─ GET /health        │
    └────────┬───────────────┘
             │ Calls OpenWeatherMap
             ▼
    ┌─────────────────────┐
    │ OpenWeatherMap API  │
    │ Returns weather data│
    └─────────────────────┘
             ▲
             │
         Returns to FastAPI
             │
             ▼
         FastAPI formats response
             │
             ▼
         Sends back to Dialogflow
             │
             ▼
         User sees: "🌤️ 28°C, Sunny"
```

---

## Complete Step-by-Step Integration

### Part 1: FastAPI Setup (5 minutes)

#### 1.1 - Create Project
```bash
mkdir weather-bot-api
cd weather-bot-api
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux
```

#### 1.2 - Install Packages
```bash
pip install fastapi uvicorn httpx python-dotenv
```

#### 1.3 - Create Files

**main.py** (Copy the provided code)
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

WEATHER_API_KEY = "ff09f16654861261ebb9d82eb601336e"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5"

@app.post("/webhook")
async def webhook(request: Request):
    # ... code here ...
```

**requirements.txt** (Copy the provided file)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.2
python-dotenv==1.0.0
```

#### 1.4 - Test Locally
```bash
python main.py
```

Visit: `http://127.0.0.1:8000/docs` (Swagger UI) ✅

---

### Part 2: Expose with ngrok (2 minutes)

```bash
# Terminal 2 (keep main.py running in Terminal 1)
cd path/to/ngrok
ngrok http 8000
```

**You'll see:**
```
Forwarding    https://abc123.ngrok.io -> http://127.0.0.1:8000
```

**COPY THIS URL** - You'll need it! 👆

---

### Part 3: Dialogflow Setup (10 minutes)

#### 3.1 - Create Agent
1. Go to: https://dialogflow.cloud.google.com/
2. Click **"Create Agent"**
3. Name: `Weather Bot`
4. Language: English
5. Click **"Create"** ✅

#### 3.2 - Create Intent #1: CurrentWeather

1. Click **"Intents"** → **"Create Intent"**
2. Name: `CurrentWeather`
3. **Training Phrases** (Add all these):
   - "What is the weather in Lahore"
   - "What's the weather in Karachi"
   - "Tell me weather in London"
   - "Current weather in Paris"
   - "Weather in Tokyo"
   - "Current conditions in New York"
   - (Add at least 6-8 variations)

4. **Action and Parameters**:
   - Click "Add parameter"
   - **Name**: `city`
   - **Entity**: `@sys.geo-city`
   - Check **"REQUIRED"** ✅
   - **Prompt**: "Which city?"

5. **Fulfillment**:
   - Check ✅ "Enable webhook call for this intent"
   - Click **"Save"** ✅

#### 3.3 - Create Intent #2: WeatherForecast

1. Click **"Intents"** → **"Create Intent"**
2. Name: `WeatherForecast`
3. **Training Phrases**:
   - "Weather forecast for Lahore"
   - "Tell me forecast for next 8 days"
   - "What will be the weather in Karachi"
   - "Forecast for London"
   - "8 day forecast for Paris"
   - "Show me forecast for Tokyo"
   - (Add at least 6-8 variations)

4. **Action and Parameters**:
   - Click "Add parameter"
   - **Name**: `city`
   - **Entity**: `@sys.geo-city`
   - Check **"REQUIRED"** ✅
   - **Prompt**: "Which city?"

5. **Fulfillment**:
   - Check ✅ "Enable webhook call for this intent"
   - Click **"Save"** ✅

#### 3.4 - Setup Webhook (CRITICAL!)

1. Click **"Fulfillment"** (Left Sidebar)
2. Toggle **"Webhook"** to **ON** (blue switch)
3. In **URL** field, paste:
   ```
   https://abc123.ngrok.io/webhook
   ```
   (Replace abc123 with YOUR ngrok URL)
4. Click **"Save"** ✅

**⚠️ IMPORTANT**: Update this every time you restart ngrok!

---

### Part 4: Test Integration (5 minutes)

#### Test 1: Health Check
Open in browser:
```
http://127.0.0.1:8000/health
```

Should see:
```json
{
  "status": "Weather Bot API is running! ✅",
  "framework": "FastAPI",
  "version": "1.0.0"
}
```

✅ API is working!

#### Test 2: Swagger UI
Open in browser:
```
http://127.0.0.1:8000/docs
```

- Click **"POST /webhook"**
- Click **"Try it out"**
- Paste:
```json
{
  "queryResult": {
    "parameters": {
      "city": "Lahore"
    }
  }
}
```
- Click **"Execute"**
- See weather response! ✅

#### Test 3: Dialogflow Simulator
1. In Dialogflow, look for chat window (right side)
2. Type: `"What is the weather in Lahore?"`
3. Press Enter
4. Bot should respond with weather! ✅

**Try these:**
```
You: "What's the weather in Karachi?"
Bot: [Shows current weather]

You: "Weather forecast for London"
Bot: [Shows 8-day forecast]

You: "Current weather in Paris"
Bot: [Shows current weather]

You: "Forecast for Tokyo"
Bot: [Shows forecast]
```

---

## How Dialogflow Sends Data to FastAPI

### Request Format
Dialogflow sends this JSON to your webhook:

```json
{
  "queryResult": {
    "parameters": {
      "city": "Lahore",
      "date": null
    }
  }
}
```

### Your FastAPI Receives It
```python
@app.post("/webhook")
async def webhook(request: Request):
    request_body = await request.json()
    # request_body now contains the data above
    
    parameters = request_body.get('queryResult', {}).get('parameters', {})
    city = parameters.get('city', 'London')  # "Lahore"
    date_str = parameters.get('date', None)  # null
    
    # Get weather for Lahore
    response = await get_current_weather(city)
```

### Your FastAPI Responds
```python
dialogflow_response = {
    "fulfillmentText": "🌤️ Current Weather in Lahore...\n32°C, Sunny"
}
return JSONResponse(dialogflow_response)
```

### Dialogflow Shows User
```
Bot: 🌤️ Current Weather in Lahore...
     32°C, Sunny ☀️
```

---

## Data Flow Example

### Scenario: User asks for current weather

```
1. USER TYPES:
   "What is the weather in Lahore?"

2. DIALOGFLOW UNDERSTANDS:
   - Intent: CurrentWeather
   - City: Lahore
   - Date: (none - means current)

3. DIALOGFLOW SENDS TO YOUR API:
   POST https://abc123.ngrok.io/webhook
   {
     "queryResult": {
       "parameters": {
         "city": "Lahore",
         "date": null
       }
     }
   }

4. YOUR FASTAPI PROCESSES:
   - Receives request
   - Extracts: city = "Lahore"
   - Calls OpenWeatherMap API
   - Gets: temperature, condition, humidity, etc.
   - Formats response

5. YOUR FASTAPI RETURNS:
   {
     "fulfillmentText": "🌤️ Current Weather in Lahore\n
     ━━━━━━━━━━━━━━━━━\n
     🌡️ Temperature: 32°C\n
     ☁️ Condition: Sunny\n
     💧 Humidity: 65%"
   }

6. DIALOGFLOW SHOWS USER:
   Bot: 🌤️ Current Weather in Lahore
        ━━━━━━━━━━━━━━━━━
        🌡️ Temperature: 32°C
        ☁️ Condition: Sunny
        💧 Humidity: 65%
```

---

## Debugging

### Check FastAPI Terminal
Your FastAPI terminal will show logs:
```
📍 Received request for city: Lahore, date: None
✅ Response sent: 🌤️ Current Weather in Lahore...
```

### Check if Dialogflow Sends Request
Add this to your FastAPI:
```python
@app.post("/webhook")
async def webhook(request: Request):
    try:
        request_body = await request.json()
        print("DEBUG: Received from Dialogflow:")
        print(request_body)  # See what Dialogflow sent
        # ... rest of code
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "Webhook connection failed" | Check ngrok URL in Dialogflow matches ngrok output |
| "City not found" | City name might be unrecognized - try different spelling |
| "API error" | Check API key, internet connection, OpenWeatherMap status |
| No response from bot | Check FastAPI is running (`python main.py`) |
| ngrok URL expired | Restart ngrok, update URL in Dialogflow |

---

## Performance Tips

1. **Use Async**: FastAPI automatically handles multiple requests ⚡
2. **Timeout**: Add timeout to API calls
   ```python
   async with httpx.AsyncClient(timeout=10.0) as client:
       response = await client.get(url)
   ```

3. **Caching**: Cache weather data for same city in same hour
   ```python
   from functools import lru_cache
   @lru_cache(maxsize=100)
   async def get_current_weather(city: str):
       # ... code ...
   ```

---

## Security Best Practices

1. **Hide API Key** in `.env`:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
   ```

2. **Add to `.gitignore`**:
   ```
   .env
   __pycache__/
   venv/
   ```

3. **Don't commit `main.py` with exposed API key!**

4. **Validate Input**:
   ```python
   if not city or len(city) > 100:
       return "Invalid city"
   ```

---

## Next Steps

1. ✅ FastAPI running locally
2. ✅ ngrok exposing your API
3. ✅ Dialogflow intents created
4. ✅ Webhook URL configured
5. ✅ Both intents tested in Simulator
6. ⏭️ Record demo video (see Recording Guide)
7. ⏭️ Push to GitHub
8. ⏭️ Submit!

---

## Useful Links

- FastAPI Docs: https://fastapi.tiangolo.com/
- Dialogflow Docs: https://cloud.google.com/dialogflow/docs
- OpenWeatherMap API: https://openweathermap.org/api
- ngrok: https://ngrok.com/

---

You're all set! 🚀 The integration is complete!
