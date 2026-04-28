# Weather Bot API - FastAPI Setup Guide

## Why FastAPI? 🚀

FastAPI is **perfect** for your Dialogflow webhook because:
- ✅ **Async/Await** - Handles multiple requests simultaneously
- ✅ **Built-in Documentation** - Auto-generated API docs at `/docs`
- ✅ **Type Hints** - Python type hints for better code quality
- ✅ **Fast** - One of the fastest Python frameworks
- ✅ **Easy to Learn** - Clean and intuitive syntax

---

## Quick Start (Copy & Paste)

### Step 1: Create Project Folder
```bash
# Create a new folder
mkdir weather-bot-api
cd weather-bot-api
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Packages
```bash
pip install fastapi uvicorn httpx python-dotenv
```

**What each package does:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server to run FastAPI
- `httpx` - Async HTTP client (like requests but async)
- `python-dotenv` - For environment variables

### Step 4: Save the Code
- Save the provided `main.py` file in your `weather-bot-api` folder

### Step 5: Create .env File (Optional but Recommended)
Create a file called `.env` in your project folder:
```
WEATHER_API_KEY=ff09f16654861261ebb9d82eb601336e
```

Or just use the API key directly in the code (as provided).

### Step 6: Run the API
```bash
python main.py
```

Or:
```bash
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

✅ Your API is running!

---

## Step 7: Access API Documentation

Open in browser:
```
http://127.0.0.1:8000/docs
```

You'll see **Swagger UI** with:
- All your endpoints listed
- Interactive testing interface
- Request/response examples
- Type hints for parameters

This is **AMAZING** for testing! 🎉

---

## Step 8: Expose with ngrok

```bash
# In a new terminal/command prompt
cd path/to/ngrok
ngrok http 8000
```

You'll see:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

**Copy this URL** - use it in Dialogflow!

---

## Testing Your API

### Option 1: Using Swagger UI (Best!)
1. Go to: `http://127.0.0.1:8000/docs`
2. Click on `POST /webhook`
3. Click "Try it out"
4. Paste this JSON:
```json
{
  "queryResult": {
    "parameters": {
      "city": "Lahore"
    }
  }
}
```
5. Click "Execute"
6. See the response! ✅

### Option 2: Health Check in Browser
Go to: `http://127.0.0.1:8000/health`

Should see:
```json
{
  "status": "Weather Bot API is running! ✅",
  "framework": "FastAPI",
  "version": "1.0.0"
}
```

### Option 3: Using curl
```bash
curl -X POST http://127.0.0.1:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "queryResult": {
      "parameters": {
        "city": "Lahore"
      }
    }
  }'
```

### Option 4: Using Python
```python
import httpx
import asyncio

async def test():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/webhook",
            json={
                "queryResult": {
                    "parameters": {
                        "city": "Lahore"
                    }
                }
            }
        )
        print(response.json())

asyncio.run(test())
```

---

## FastAPI vs Flask - Key Differences

| Feature | FastAPI | Flask |
|---------|---------|-------|
| Async Support | ✅ Built-in | ❌ Basic |
| Performance | ⚡ Faster | 🐢 Slower |
| Documentation | 📚 Auto-generated | ❌ Manual |
| Type Hints | ✅ Full support | ❌ Limited |
| Learning Curve | 📈 Medium | 📈 Easy |
| Best For | APIs, Webhooks | Web apps, Simple sites |

---

## FastAPI Code Explanation

### 1. Import Statements
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx  # Async HTTP client
```

### 2. Create App
```python
app = FastAPI()
```

### 3. Define Routes
```python
@app.get("/health")  # GET endpoint
async def health():
    return {"status": "ok"}

@app.post("/webhook")  # POST endpoint
async def webhook(request: Request):
    data = await request.json()  # Async file reading!
    return JSONResponse({"result": "ok"})
```

### 4. Async Functions
```python
async def get_current_weather(city: str) -> str:
    """
    async = can handle multiple requests at once
    This doesn't block! FastAPI magic 🪄
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()
```

---

## Running on Different Ports

Default is port 8000. To change:

```bash
# Run on port 5000
uvicorn main:app --reload --port 5000

# Run on port 3000
uvicorn main:app --reload --port 3000
```

Then update ngrok:
```bash
ngrok http 5000
```

---

## Project Structure

```
weather-bot-api/
│
├── main.py                 # Your FastAPI application
├── requirements.txt        # Dependencies
├── .env                   # API key (don't commit)
├── .gitignore            # Ignore .env and __pycache__
├── README.md             # Documentation
└── venv/                 # Virtual environment (don't commit)
```

---

## Troubleshooting

### Q: "ModuleNotFoundError: No module named 'fastapi'"
**A**: Install it:
```bash
pip install fastapi uvicorn httpx
```

### Q: "Port 8000 already in use"
**A**: Run on different port:
```bash
uvicorn main:app --port 8001
```

### Q: "API not responding from Dialogflow"
**A**: 
- Make sure FastAPI is running
- Check ngrok is running and URL is correct
- Verify webhook URL in Dialogflow matches ngrok URL
- Check terminal for error messages

### Q: "Error fetching weather"
**A**:
- Verify API key is correct
- Check internet connection
- Make sure city name is spelled correctly

### Q: "Async error"
**A**: Make sure you're using `async with httpx.AsyncClient()` for HTTP requests.

---

## Deployment

### Heroku
```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port 8000" > Procfile

# Create requirements.txt
pip freeze > requirements.txt

# Deploy
git push heroku main
```

### Docker
```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Google Cloud Run
```bash
gcloud run deploy weather-bot \
  --source . \
  --platform managed \
  --region us-central1
```

---

## Environment Variables (Best Practice)

Update `main.py` to use `.env`:

```python
import os
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
```

Create `.env`:
```
WEATHER_API_KEY=ff09f16654861261ebb9d82eb601336e
```

Add to `.gitignore`:
```
.env
__pycache__/
*.pyc
venv/
.DS_Store
```

---

## Next Steps

1. ✅ Run the API locally
2. ✅ Test using Swagger UI (`/docs`)
3. ✅ Start ngrok
4. ✅ Setup Dialogflow webhook
5. ✅ Test with Dialogflow
6. ✅ Record demo
7. ✅ Push to GitHub

---

## Useful Commands

```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install packages
pip install fastapi uvicorn httpx python-dotenv

# Run with auto-reload (development)
uvicorn main:app --reload

# Run production
uvicorn main:app --host 0.0.0.0 --port 8000

# Generate requirements.txt
pip freeze > requirements.txt

# Check if running
curl http://127.0.0.1:8000/health
```

---

Good luck! FastAPI is awesome! 🚀
