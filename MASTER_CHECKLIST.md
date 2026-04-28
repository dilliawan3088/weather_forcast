# 🎯 Weather Bot Project - Master Checklist

**Your API Key:** `ff09f16654861261ebb9d82eb601336e` ✅

---

## PHASE 1: Setup Your Computer 💻

### Installation
- [ ] Python 3.7+ installed
- [ ] Virtual environment created: `python -m venv venv`
- [ ] Virtual environment activated: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
- [ ] Packages installed: `pip install fastapi uvicorn httpx python-dotenv`

### Download Tools
- [ ] ngrok downloaded: https://ngrok.com/download
- [ ] OBS Studio downloaded: https://obsproject.com/ (for recording)
- [ ] Code editor ready (VS Code recommended)

### API & Accounts
- [ ] ✅ OpenWeatherMap API Key: `ff09f16654861261ebb9d82eb601336e`
- [ ] ✅ Google account for Dialogflow
- [ ] ✅ GitHub account created

---

## PHASE 2: Create Your FastAPI Backend 🔧

### Project Setup
- [ ] Create folder: `weather-bot-api`
- [ ] Create `main.py` (copy the provided code)
- [ ] Create `requirements.txt` (copy the provided file)
- [ ] Create `.env` file with your API key (optional)

### Testing FastAPI
- [ ] Run: `python main.py`
- [ ] See in terminal: `Uvicorn running on http://127.0.0.1:8000`
- [ ] Open browser: `http://127.0.0.1:8000/docs` (Swagger UI)
- [ ] Swagger UI loads successfully ✅
- [ ] Test `/health` endpoint
- [ ] Test `/webhook` endpoint with sample JSON

### Expose with ngrok
- [ ] Open new Command Prompt
- [ ] Go to ngrok folder
- [ ] Run: `ngrok http 8000`
- [ ] See: `Forwarding https://abc123.ngrok.io -> http://127.0.0.1:8000`
- [ ] **COPY THE HTTPS URL** ← You'll need this!
- [ ] Keep ngrok running (don't close this window)

---

## PHASE 3: Setup Dialogflow 🤖

### Create Dialogflow Agent
- [ ] Go to: https://dialogflow.cloud.google.com/
- [ ] Click "Create Agent"
- [ ] Name: `Weather Bot`
- [ ] Language: English
- [ ] Click "Create"
- [ ] Agent created successfully ✅

### Create Intent #1: CurrentWeather

#### Training Phrases (Add all of these):
- [ ] "What is the weather in Lahore"
- [ ] "What's the weather in Karachi"
- [ ] "Tell me current weather in London"
- [ ] "Weather in Paris"
- [ ] "Current weather in New York"
- [ ] "What is the weather in Tokyo"
- [ ] "Current conditions in Dubai"

#### Action and Parameters:
- [ ] Click "Add parameter"
- [ ] Parameter name: `city`
- [ ] Entity: `@sys.geo-city`
- [ ] Check "REQUIRED" ✅
- [ ] Prompt: "Which city?"

#### Fulfillment:
- [ ] Check ✅ "Enable webhook call for this intent"
- [ ] Click "Save" ✅

### Create Intent #2: WeatherForecast

#### Training Phrases (Add all of these):
- [ ] "Weather forecast for Lahore"
- [ ] "Tell me forecast for next 8 days"
- [ ] "What will be the weather in Karachi"
- [ ] "Forecast for London"
- [ ] "8 day forecast for Paris"
- [ ] "Show me forecast for Tokyo"
- [ ] "Weather forecast for Dubai next week"

#### Action and Parameters:
- [ ] Click "Add parameter"
- [ ] Parameter name: `city`
- [ ] Entity: `@sys.geo-city`
- [ ] Check "REQUIRED" ✅
- [ ] Prompt: "Which city?"

#### Fulfillment:
- [ ] Check ✅ "Enable webhook call for this intent"
- [ ] Click "Save" ✅

### Setup Webhook
- [ ] Click "Fulfillment" (left sidebar)
- [ ] Toggle "Webhook" to ON (blue switch)
- [ ] Paste your ngrok URL: `https://abc123.ngrok.io/webhook`
- [ ] Click "Save" ✅

---

## PHASE 4: Integration Testing 🧪

### Test in Dialogflow Simulator
- [ ] **Test 1 - Current Weather**
  - [ ] Type: "What is the weather in Lahore?"
  - [ ] Bot responds with current weather ✅
  - [ ] Shows temperature, humidity, etc. ✅

- [ ] **Test 2 - Forecast**
  - [ ] Type: "Weather forecast for Karachi"
  - [ ] Bot responds with 8-day forecast ✅
  - [ ] Shows dates and temperatures ✅

- [ ] **Test 3 - Different City**
  - [ ] Type: "Current weather in London"
  - [ ] Bot responds with London weather ✅

- [ ] **Test 4 - Another Forecast**
  - [ ] Type: "Forecast for Paris"
  - [ ] Bot responds with Paris forecast ✅

### Verify Everything Works
- [ ] No "webhook" errors in responses
- [ ] Bot understands natural language queries
- [ ] Bot returns real weather data
- [ ] Different cities work correctly
- [ ] Both current and forecast requests work

---

## PHASE 5: Record Demo Video 🎥

### Setup OBS Studio
- [ ] Download OBS Studio: https://obsproject.com/
- [ ] Install OBS Studio
- [ ] Open OBS Studio

### Create Recording
- [ ] Click "Start Recording"
- [ ] Make Dialogflow window visible
- [ ] **Perform these interactions** (speak out loud explaining):

1. [ ] "What is the weather in Lahore?"
   - [ ] Wait for response
   - [ ] Explain: "The bot shows current weather with temperature, humidity, wind speed"

2. [ ] "Weather forecast for Karachi"
   - [ ] Wait for response
   - [ ] Explain: "The bot shows 8-day forecast with daily temperatures"

3. [ ] "Tell me current weather in London"
   - [ ] Wait for response
   - [ ] Explain: "The bot works for any city globally"

4. [ ] "Forecast for Paris"
   - [ ] Wait for response
   - [ ] Explain: "Demonstrating forecast functionality again"

- [ ] Click "Stop Recording"
- [ ] Save video: `weather-bot-demo.mp4`

### Video Quality Checklist
- [ ] Duration: 2-3 minutes ✅
- [ ] Audio is clear and audible ✅
- [ ] Screen is clearly visible ✅
- [ ] Shows at least 2 current weather requests ✅
- [ ] Shows at least 2 forecast requests ✅
- [ ] Shows different cities ✅
- [ ] Has voiceover explaining the process ✅

---

## PHASE 6: Prepare Code for GitHub 📝

### Update main.py (For Security)
- [ ] Open `main.py`
- [ ] Replace this line:
```python
WEATHER_API_KEY = "ff09f16654861261ebb9d82eb601336e"
```

With this:
```python
import os
from dotenv import load_dotenv
load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'ff09f16654861261ebb9d82eb601336e')
```

### Create .env File
- [ ] Create file: `.env`
- [ ] Add this line:
```
WEATHER_API_KEY=ff09f16654861261ebb9d82eb601336e
```
- [ ] This file stays on your computer (don't commit to GitHub)

### Create .gitignore File
- [ ] Create file: `.gitignore`
- [ ] Add these lines:
```
.env
__pycache__/
*.pyc
venv/
.DS_Store
*.db
```

### Files Ready for GitHub
- [ ] main.py (updated, API key not hardcoded)
- [ ] requirements.txt
- [ ] README.md (provided)
- [ ] .gitignore
- [ ] .env (local only, not committed)

---

## PHASE 7: Upload to GitHub 🚀

### Create GitHub Repository
- [ ] Go to: https://github.com
- [ ] Click "New" → "New repository"
- [ ] Repository name: `weather-bot-api`
- [ ] Description: "Weather Bot API - Google Dialogflow Integration"
- [ ] Visibility: Public
- [ ] Click "Create repository"

### Upload Files (Option 1: Git Command Line)
```bash
cd weather-bot-api
git init
git add .
git commit -m "Initial commit - Weather Bot API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/weather-bot-api.git
git push -u origin main
```

- [ ] Copy commands above
- [ ] Run in your project folder
- [ ] Files uploaded to GitHub ✅

### Upload Files (Option 2: GitHub Desktop)
- [ ] Download: https://desktop.github.com/
- [ ] Sign in with GitHub account
- [ ] "Add" → "Add Existing Repository"
- [ ] Select your `weather-bot-api` folder
- [ ] Click "Publish repository"

### Verify on GitHub
- [ ] Go to your repository URL
- [ ] See files: `main.py`, `requirements.txt`, `README.md`, `.gitignore`
- [ ] README.md displays nicely ✅
- [ ] NO `.env` file visible (it's in .gitignore) ✅
- [ ] Copy repository URL: `https://github.com/YOUR_USERNAME/weather-bot-api`

---

## PHASE 8: Export Dialogflow Agent 📦

### Export Agent
- [ ] In Dialogflow agent page
- [ ] Click ⚙️ (Settings icon)
- [ ] Click "Export and Import"
- [ ] Click "Export as ZIP"
- [ ] Save file: `weather-bot-dialogflow.zip`
- [ ] File saved successfully ✅

---

## PHASE 9: Prepare Submission 📮

### Gather All Files
- [ ] Demo video: `weather-bot-demo.mp4` ✅
- [ ] Dialogflow export: `weather-bot-dialogflow.zip` ✅
- [ ] GitHub repository URL: ✅

### Create Submission Package
- [ ] Create folder: `Weather-Bot-Submission`
- [ ] Move inside:
  - [ ] `weather-bot-demo.mp4`
  - [ ] `weather-bot-dialogflow.zip`
  - [ ] Create text file: `github-repo-link.txt` with your repo URL

### Prepare Email
Subject:
```
Weather Bot Evaluation Test Submission
```

Body:
```
Dear InteractCX Team,

Please find my Weather Bot API submission attached:

1. Demo Video: weather-bot-demo.mp4
2. Dialogflow Agent: weather-bot-dialogflow.zip
3. GitHub Repository: [PASTE YOUR REPO URL]

The API is implemented in FastAPI and integrates with Google Dialogflow ES to provide real-time weather information and forecasts.

Thank you,
[YOUR NAME]
```

Attachments:
- [ ] weather-bot-demo.mp4
- [ ] weather-bot-dialogflow.zip

---

## PHASE 10: Submit! 🎉

### Send Submission
- [ ] Email to: `submissions@interactcx.com`
- [ ] Subject: "Weather Bot Evaluation Test Submission"
- [ ] Include all attachments
- [ ] Include GitHub repo link
- [ ] Click "Send" ✅

### After Submission
- [ ] Keep your local code safe
- [ ] Keep your API key secret
- [ ] Wait for feedback from InteractCX

---

## 📋 Quick Reference

### Important Links
- Dialogflow: https://dialogflow.cloud.google.com/
- OpenWeatherMap: https://openweathermap.org/api
- GitHub: https://github.com
- ngrok: https://ngrok.com/

### Important Commands
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install packages
pip install fastapi uvicorn httpx python-dotenv

# Run FastAPI
python main.py

# Run ngrok (new terminal)
ngrok http 8000

# Upload to GitHub
git add .
git commit -m "Your message"
git push
```

### Important URLs (During Development)
- Swagger UI: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health
- Dialogflow: https://dialogflow.cloud.google.com/

### Important Files
- FastAPI Code: `main.py`
- Dependencies: `requirements.txt`
- Environment Variables: `.env` (local only)
- Gitignore: `.gitignore`
- API Key: `ff09f16654861261ebb9d82eb601336e`

---

## ⏱️ Timeline

- **Setup**: 15 minutes
- **FastAPI Development**: 10 minutes (code already provided)
- **Dialogflow Setup**: 10 minutes
- **Testing**: 10 minutes
- **Recording Demo**: 10 minutes
- **GitHub Upload**: 5 minutes
- **Submission**: 5 minutes

**Total: ~65 minutes** ⏱️

---

## 🚀 You've Got This!

**Status**: Ready to Start! 

All files are provided:
- ✅ main.py (FastAPI code)
- ✅ requirements.txt
- ✅ README.md
- ✅ Setup guides
- ✅ Integration guide

**Just follow the checklist step by step!**

---

## Need Help?

1. **FastAPI Issue?** → Check FASTAPI_SETUP.md
2. **Dialogflow Issue?** → Check DIALOGFLOW_SETUP.md
3. **Integration Issue?** → Check FASTAPI_DIALOGFLOW_INTEGRATION.md
4. **Quick Start?** → Read FASTAPI_QUICK_START.md

Good luck! 🎉
