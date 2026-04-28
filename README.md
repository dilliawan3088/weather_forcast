# 🌤️ Weather Bot API

A Flask-based REST API that provides real-time weather information and 8-day forecasts for any city worldwide. Built to integrate with Google Dialogflow ES chatbot.

## Features

✅ **Current Weather** - Get real-time weather data for any city
✅ **8-Day Forecast** - Weather forecast for the next 8 days
✅ **Detailed Information** - Temperature, humidity, wind speed, pressure, and more
✅ **Error Handling** - Graceful error messages for invalid cities
✅ **Dialogflow Integration** - Easy webhook integration with Dialogflow ES
✅ **Fast & Reliable** - Uses OpenWeatherMap API

## Tech Stack

- **Backend**: Python 3.x
- **Framework**: Flask
- **API**: OpenWeatherMap API
- **Hosting**: Can be hosted on any server or locally with ngrok

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- OpenWeatherMap API Key (free from https://openweathermap.org/api)
- ngrok (for local testing with Dialogflow)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/weather-bot-api.git
cd weather-bot-api
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flask requests
```

### 4. Setup Environment Variables
Create a `.env` file in the root directory:
```
WEATHER_API_KEY=your_api_key_here
```

Or directly edit the `WEATHER_API_KEY` variable in `app.py`

## Usage

### Running Locally

```bash
python app.py
```

The API will start on: `http://localhost:5000`

### Testing the API

#### Health Check
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "Weather Bot API is running! ✅"
}
```

#### Get Current Weather
```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "queryResult": {
      "parameters": {
        "city": "Lahore"
      }
    }
  }'
```

Response:
```
🌤️ *Current Weather in Lahore*
━━━━━━━━━━━━━━━━━━━━
🌡️ Temperature: 28.5°C
🤔 Feels Like: 30.2°C
☁️ Condition: Clear (clear sky)
💧 Humidity: 65%
💨 Wind Speed: 2.1 m/s
🔽 Pressure: 1010 hPa
━━━━━━━━━━━━━━━━━━━━
```

#### Get Weather Forecast
```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "queryResult": {
      "parameters": {
        "city": "Lahore",
        "date": "2024-05-01"
      }
    }
  }'
```

## API Endpoints

### POST /webhook
Receives requests from Dialogflow and returns weather information.

**Request Body:**
```json
{
  "queryResult": {
    "parameters": {
      "city": "London",
      "date": "2024-05-01"  // Optional
    }
  }
}
```

**Response:**
```json
{
  "fulfillmentText": "🌤️ *Current Weather in London*..."
}
```

### GET /health
Health check endpoint to verify API is running.

**Response:**
```json
{
  "status": "Weather Bot API is running! ✅"
}
```

## Dialogflow Integration

### Setup Webhook URL
1. In Dialogflow, go to **Fulfillment**
2. Enable **Webhook**
3. Add your API URL (with ngrok for local testing):
   ```
   https://abc123.ngrok.io/webhook
   ```

### Create Intents
1. **CurrentWeather Intent**
   - Training phrases: "What is the weather in Lahore?" etc.
   - Parameter: `city` (@sys.geo-city) - Required
   - Enable webhook

2. **WeatherForecast Intent**
   - Training phrases: "Weather forecast for Lahore" etc.
   - Parameter: `city` (@sys.geo-city) - Required
   - Enable webhook

## Using ngrok for Local Testing

```bash
ngrok http 5000
```

This exposes your local API publicly. Use the HTTPS URL in Dialogflow.

## File Structure

```
weather-bot-api/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (don't commit)
├── .gitignore           # Git ignore file
├── README.md            # This file
└── docs/
    ├── SETUP_GUIDE.md
    └── DIALOGFLOW_SETUP.md
```

## Error Handling

The API handles the following errors gracefully:

- **Invalid City**: Returns "City 'X' not found. Please check the spelling and try again."
- **Network Error**: Returns error message with details
- **API Error**: Returns error message if OpenWeatherMap API is unavailable

## Supported Cities

The API supports all cities available in OpenWeatherMap database. Some examples:

- Lahore, Karachi, Islamabad (Pakistan)
- London, Paris, Berlin (Europe)
- New York, Los Angeles (USA)
- Tokyo, Beijing, Mumbai (Asia)
- Sydney, Dubai, Singapore
- And 200,000+ more cities!

## Deployment

### Option 1: Heroku (Free)
```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Create requirements.txt
pip freeze > requirements.txt

# Deploy to Heroku
git push heroku main
```

### Option 2: Vercel, AWS, Google Cloud, Azure
Follow their respective deployment guides.

## API Key Safety

⚠️ **NEVER commit your API key to GitHub!**

Use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
```

Create `.env` file:
```
WEATHER_API_KEY=your_key_here
```

Add to `.gitignore`:
```
.env
__pycache__/
venv/
```

## Troubleshooting

### Q: "City not found" error
**A**: Check the spelling. The city must exist in OpenWeatherMap database.

### Q: "Webhook error" from Dialogflow
**A**: 
- Make sure your Flask app is running
- Verify the webhook URL in Dialogflow is correct
- Check that ngrok is running (if using local)

### Q: API key error
**A**: Verify your OpenWeatherMap API key is correct and not expired.

### Q: Port 5000 already in use
**A**: Change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

## Future Enhancements

- [ ] Add weather alerts
- [ ] Add historical weather data
- [ ] Support multiple languages
- [ ] Add weather icons/emojis based on conditions
- [ ] Cache weather data for performance
- [ ] Add rate limiting
- [ ] Database integration for user preferences

## License

This project is open source and available under the MIT License.

## Author

Created for InteractCX Evaluation Test

## Contact

For queries or issues:
- Email: candidatequeries@interactcx.com
- GitHub: https://github.com/YOUR_USERNAME

## Acknowledgments

- OpenWeatherMap API for weather data
- Google Dialogflow for chatbot platform
- Flask for the web framework

---

Made with ❤️ for InteractCX
