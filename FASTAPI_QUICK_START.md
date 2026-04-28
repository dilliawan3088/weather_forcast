# ⚡ FastAPI Weather Bot - 30 Second Start

## Just Want to Get Running? Do This:

### Terminal 1: Setup
```bash
mkdir weather-bot-api
cd weather-bot-api
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install fastapi uvicorn httpx python-dotenv
```

### Save main.py
Copy the provided `main.py` file into your folder

### Terminal 1: Start FastAPI
```bash
python main.py
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2: Start ngrok (New Terminal)
```bash
cd path/to/ngrok
ngrok http 8000
```

**Output:**
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

✅ **You're Done!** Copy that https URL to Dialogflow webhook.

---

## Test It Works

**Open Browser:**
```
http://127.0.0.1:8000/docs
```

You'll see **Swagger UI** - interactive API testing! 

**Click "POST /webhook" → "Try it out"**

Paste:
```json
{
  "queryResult": {
    "parameters": {
      "city": "Lahore"
    }
  }
}
```

**Click "Execute"** → See weather response! ✅

---

## Use This in Dialogflow

**Webhook URL:**
```
https://abc123.ngrok.io/webhook
```

**Done!** Your bot will now use this API! 🎉

---

## File Structure You Need

```
weather-bot-api/
├── main.py              ← The code
├── requirements.txt     ← Dependencies
└── venv/               ← Virtual environment
```

That's it! Everything else is optional.

---

## Common Issues

| Problem | Solution |
|---------|----------|
| Port 8000 in use | `uvicorn main:app --port 8001` |
| Module not found | `pip install fastapi uvicorn httpx` |
| City not found | Check spelling in training phrases |
| Webhook error | Verify URL in Dialogflow matches ngrok |
| ngrok expired | Restart ngrok, update Dialogflow URL |

---

## What's Happening?

```
User: "What's the weather in Lahore?"
  ↓
Dialogflow catches it
  ↓
Sends to: https://abc123.ngrok.io/webhook
  ↓
Your FastAPI (main.py) receives it
  ↓
Calls OpenWeatherMap API
  ↓
Gets: "28°C, Sunny, etc."
  ↓
Sends back to Dialogflow
  ↓
User sees: "🌤️ Current Weather in Lahore: 28°C, Sunny"
```

---

**You're ready!** 🚀

Next step: Setup Dialogflow intents (see DIALOGFLOW_SETUP.md)
