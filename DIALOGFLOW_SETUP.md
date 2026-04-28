# Dialogflow ES - Complete Setup Guide

## Step 1: Create Dialogflow Agent

1. Go to: https://dialogflow.cloud.google.com/
2. Sign in with your Google account
3. Click **"Create Agent"** button
4. Fill in:
   - **Agent Name**: `Weather Bot`
   - **Default Language**: English
   - **Default Timezone**: Your timezone
5. Click **"Create"**
6. Wait for agent to be created ✅

---

## Step 2: Create Intent #1 - Current Weather

### In Dialogflow, Click: **Intents** → **Create Intent**

#### Basic Info:
- **Intent Name**: `CurrentWeather`
- **Display Name**: `CurrentWeather`

#### Training Phrases (Copy & Paste These):
Add these by typing in the input field and pressing Enter:

```
What is the current weather in Lahore
What's the weather in Karachi
Tell me current weather in London
Weather in Paris
Current weather in New York
What is the weather in Tokyo
Weather in Berlin
Current conditions in Mumbai
Tell me the weather in Dubai
```

#### Action and Parameters:

1. Scroll down to **"Action and parameters"** section
2. Click **"Add parameter"**
3. Fill in:
   - **Parameter Name**: `city`
   - **Entity**: Select `@sys.geo-city`
   - **Check "REQUIRED"** checkbox
   - **Prompts**: "Which city would you like the weather for?"

#### Fulfillment:

1. Scroll down to **"Fulfillment"** section
2. Check: ✅ **"Enable webhook call for this intent"**

#### Save:
Click **"Save"** button at top

---

## Step 3: Create Intent #2 - Weather Forecast

### Click: **Intents** → **Create Intent**

#### Basic Info:
- **Intent Name**: `WeatherForecast`
- **Display Name**: `WeatherForecast`

#### Training Phrases:

```
Weather forecast for Lahore
Tell me forecast for next 8 days
What will be the weather in Karachi
Forecast for London
8 day forecast for Paris
Show me weather forecast in New York
Weather forecast for the next week in Tokyo
What's the forecast in Berlin
Forecast in Mumbai
```

#### Action and Parameters:

1. Click **"Add parameter"**
2. Fill in:
   - **Parameter Name**: `city`
   - **Entity**: Select `@sys.geo-city`
   - **Check "REQUIRED"** checkbox
   - **Prompts**: "Which city would you like the forecast for?"

#### Fulfillment:

1. Check: ✅ **"Enable webhook call for this intent"**

#### Save:
Click **"Save"** button

---

## Step 4: Setup Webhook (IMPORTANT!)

### Click: **Fulfillment** (Left Sidebar)

1. Toggle **"Webhook"** to **ON** (blue switch)
2. In **"URL"** field, paste your ngrok URL:
   ```
   https://abc123.ngrok.io/webhook
   ```
   (Replace abc123 with your actual ngrok URL)

3. Click **"Save"** at bottom

⚠️ **IMPORTANT**: Update this URL every time you restart ngrok!

---

## Step 5: Test Your Bot

### Using Dialogflow Simulator:

1. On the right side, you'll see a **chat window** (Simulator)
2. Type: `"What is the weather in Lahore?"`
3. Press Enter
4. The bot should respond with current weather! ✅

### Test Different Queries:

✅ Test 1:
```
You: "What's the weather in Karachi?"
Bot: [Shows current weather for Karachi]
```

✅ Test 2:
```
You: "Weather forecast for London"
Bot: [Shows 8-day forecast]
```

✅ Test 3:
```
You: "Tell me the weather in Paris"
Bot: [Shows current weather]
```

---

## Troubleshooting

### Issue: Bot says "Something went wrong"
- Check if your Flask API is running
- Verify ngrok is running and URL is correct
- Check the webhook URL in Dialogflow matches your ngrok URL

### Issue: Bot doesn't recognize city
- Make sure the city name is spelled correctly
- Dialogflow should highlight the city as a recognized entity (blue highlight)

### Issue: "Webhook error"
- Check terminal where Flask is running for error messages
- Verify API key is correct in app.py
- Make sure Flask app.py is running on port 5000

### Issue: ngrok URL expired
- Restart ngrok: `ngrok http 5000`
- Update the URL in Dialogflow Fulfillment
- Test again

---

## Final Checklist Before Demo

- ✅ Flask API running (`python app.py`)
- ✅ ngrok running (`ngrok http 5000`)
- ✅ Webhook URL in Dialogflow matches ngrok URL
- ✅ Two intents created (CurrentWeather & WeatherForecast)
- ✅ Both intents have "Webhook call enabled"
- ✅ Both intents have "city" parameter set as REQUIRED
- ✅ Bot responds correctly in Simulator
- ✅ API key is valid and working

---

## Recording Your Demo

Use OBS Studio (free):

1. **Download**: https://obsproject.com/
2. **Open OBS Studio**
3. **Click "Start Recording"**
4. **Open Dialogflow Simulator** (in Dialogflow chat)
5. **Have conversations** with your bot:
   - "What is the weather in Lahore?"
   - "Weather forecast for Karachi"
   - "Tell me current weather in London"
   - "8 day forecast for Paris"
6. **Explain what you're doing** (speak out loud)
7. **Click "Stop Recording"**
8. **Save the video file**

**Demo should show:**
- Bot understanding natural language
- Bot providing correct weather data
- Bot handling both current weather and forecast requests
- Bot handling different cities

---

## Ready to Submit?

Your deliverables:
1. ✅ Demo video (recorded with OBS)
2. ✅ Python API code (app.py) on GitHub
3. ✅ Dialogflow agent exported as JSON

**Export Dialogflow Agent:**
1. Click ⚙️ (Settings) → **Export and Import**
2. Click **Export as ZIP**
3. Save this ZIP file

**Email to**: submissions@interactcx.com
- Subject: Weather Bot Evaluation Test Submission
- Attachments: 
  - Demo video
  - Dialogflow ZIP export
  - Link to GitHub repository

---

Good luck! You've got this! 🎉
