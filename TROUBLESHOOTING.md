# 🆘 Troubleshooting Guide - Weather Bot

## FastAPI Issues

### Issue 1: "ModuleNotFoundError: No module named 'fastapi'"

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install packages
pip install fastapi uvicorn httpx python-dotenv
```

---

### Issue 2: "Port 8000 already in use"

**Error Message:**
```
OSError: [Errno 48] Address already in use
```

**Solution 1: Use different port**
```bash
uvicorn main:app --port 8001
```

**Solution 2: Kill process using port 8000**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID YOUR_PID /F

# Mac/Linux
lsof -i :8000
kill -9 YOUR_PID
```

---

### Issue 3: "python: command not found"

**Error Message:**
```
python: command not found
```

**Solution:**
```bash
# Try python3 instead
python3 main.py

# Or reinstall Python from https://www.python.org/downloads/
```

---

### Issue 4: "uvicorn not found"

**Error Message:**
```
'uvicorn' is not recognized as an internal or external command
```

**Solution:**
```bash
# Install uvicorn
pip install uvicorn

# Or run with python
python -m uvicorn main:app --reload
```

---

## ngrok Issues

### Issue 5: "ngrok command not found"

**Error Message:**
```
'ngrok' is not recognized as an internal or external command
```

**Solution:**
1. Download ngrok: https://ngrok.com/download
2. Extract the file
3. Open Command Prompt in that folder
4. Run: `ngrok http 8000`

Or add ngrok to PATH:
```bash
# Windows - Add ngrok.exe location to PATH
# Then restart Command Prompt and try again
```

---

### Issue 6: "Session expired" (ngrok)

**Error Message:**
```
ERR_NGROK_222
Session Expired
```

**Solution:**
1. Restart ngrok:
   ```bash
   ngrok http 8000
   ```
2. You'll get a new URL (e.g., `https://xyz123.ngrok.io`)
3. **Update the URL in Dialogflow**:
   - Go to Dialogflow
   - Click "Fulfillment"
   - Update webhook URL to new ngrok URL
   - Click "Save"

---

### Issue 7: "Timeout" in ngrok

**Error Message:**
```
timeout - ngrok
```

**Solution:**
- ngrok free plan has 8-hour session limit
- Just restart ngrok: `ngrok http 8000`
- Update URL in Dialogflow

---

## Dialogflow Issues

### Issue 8: "Webhook connection failed"

**Error Message:**
```
Webhook connection failed
Something went wrong
```

**Solutions:**

**Check 1: Is FastAPI running?**
```bash
# Terminal 1 should show:
INFO:     Uvicorn running on http://127.0.0.1:8000
```
If not, run: `python main.py`

**Check 2: Is ngrok running?**
```bash
# Terminal 2 should show:
Forwarding    https://abc123.ngrok.io -> http://127.0.0.1:8000
```
If not, run: `ngrok http 8000`

**Check 3: Is webhook URL correct?**
- In Dialogflow, go to "Fulfillment"
- Check webhook URL matches your ngrok URL exactly
- Should look like: `https://abc123.ngrok.io/webhook`

**Check 4: Is webhook enabled?**
- In Dialogflow, in each intent:
  - Click intent
  - Scroll to "Fulfillment"
  - Check ✅ "Enable webhook call for this intent"
  - Click "Save"

---

### Issue 9: Bot says "Something went wrong"

**Solution:**
1. Check FastAPI terminal for error messages
2. Look for lines like:
   ```
   ERROR: ... 
   ```
3. Common errors:
   - **API key wrong**: Check if you copied it correctly
   - **City not found**: Try different city spelling
   - **Internet error**: Check connection

---

### Issue 10: Bot doesn't recognize city name

**Error:**
```
Bot: I didn't understand that
```

**Solutions:**
1. **City not spelled correctly**:
   - Training phrase: "What is the weather in Lahorr?" ❌
   - Should be: "What is the weather in Lahore?" ✅

2. **City not in Dialogflow entity**:
   - Go to the intent
   - Check if "city" parameter is set to `@sys.geo-city`
   - Should highlight city names in blue

3. **City not recognized by Dialogflow**:
   - Try training phrases with common cities first
   - "London", "New York", "Tokyo" usually work
   - Smaller cities might not be recognized

4. **Test in Swagger UI first**:
   - Go to: http://127.0.0.1:8000/docs
   - Test your API before testing in Dialogflow

---

### Issue 11: "Invalid parameter" error

**Solution:**
Make sure in each intent you have:
- Parameter name: `city` (exactly)
- Entity: `@sys.geo-city` (exactly)
- Marked as REQUIRED

---

## Weather Data Issues

### Issue 12: "City not found" from API

**Error:**
```
❌ City 'Lahor' not found. Please check the spelling and try again.
```

**Solution:**
1. Check city spelling
2. Most common cities work: London, Paris, New York, Tokyo, etc.
3. Test in Swagger UI:
   - http://127.0.0.1:8000/docs
   - POST /webhook
   - Try different city names

---

### Issue 13: No weather data returned

**Problem:** Bot responds but no weather info shown

**Solution:**
1. Check API key is valid:
   ```bash
   # Visit in browser (replace YOUR_CITY and API_KEY)
   https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY
   ```

2. If you see:
   ```json
   {"cod":"401","message":"Invalid API key"}
   ```
   → Your API key is wrong

3. If you see:
   ```json
   {"cod":"404","message":"city not found"}
   ```
   → City doesn't exist

---

## Testing Issues

### Issue 14: "Cannot test in Swagger UI"

**Error:**
```
Failed to fetch
```

**Solutions:**
1. Make sure FastAPI is running: `python main.py`
2. Try refreshing the page: F5
3. Check browser console (F12) for errors
4. Try different browser (Chrome recommended)

---

### Issue 15: Different responses in different tests

**Problem:**
- Works in Swagger UI ✅
- Doesn't work in Dialogflow ❌

**Solutions:**
1. Check webhook URL in Dialogflow matches ngrok URL
2. Check both intents have webhook enabled
3. Check parameter names match exactly: `city`
4. Test different cities to see pattern
5. Check FastAPI terminal for error messages

---

## Recording Issues

### Issue 16: OBS Studio not recording

**Solutions:**
1. Check recording path:
   - Click "Settings"
   - Go to "Output"
   - Check recording path is valid

2. Check disk space (need at least 500MB)

3. Check audio:
   - Click "Settings"
   - Go to "Audio"
   - Check "Mic/Auxiliary Audio" is enabled

4. Try different output format:
   - Settings → Output → Recording Format
   - Change to "mp4" or "mov"

---

### Issue 17: Audio not recording

**Solution:**
1. Click "Settings"
2. Go to "Audio"
3. Under "Mic/Auxiliary Audio", select your microphone
4. Test audio level (see green bars when speaking)
5. Try recording again

---

## GitHub Issues

### Issue 18: "Git command not found"

**Solution:**
1. Download Git: https://git-scm.com/
2. Install Git
3. Restart Command Prompt
4. Try again: `git --version`

---

### Issue 19: "Permission denied" (GitHub)

**Error:**
```
Permission denied (publickey)
```

**Solution:**
Use HTTPS instead of SSH:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/weather-bot-api.git
```

---

### Issue 20: "API key exposed" on GitHub

**IMPORTANT - Don't panic!**

1. Immediately rotate your API key:
   - Go to OpenWeatherMap
   - Generate new API key
   - Update `.env` file locally

2. Remove from GitHub history:
   ```bash
   # This removes file from history
   git filter-branch --tree-filter 'rm -f main.py' HEAD
   ```

3. Add `.env` to `.gitignore` for future

---

## Integration Troubleshooting

### Issue 21: "Works locally but not in Dialogflow"

**Checklist:**
- [ ] FastAPI running: `python main.py`
- [ ] ngrok running: `ngrok http 8000`
- [ ] ngrok URL in Dialogflow webhook
- [ ] Both intents have webhook enabled
- [ ] Parameter names exactly: `city`
- [ ] Parameter required: `@sys.geo-city`
- [ ] No typos in webhook URL

---

### Issue 22: "Dialogflow shows different response"

**Problem:** Bot shows different output than expected

**Solutions:**
1. Check your response formatting in `main.py`
2. Look at actual response in FastAPI terminal
3. Test same request in Swagger UI
4. Compare responses

---

## Performance Issues

### Issue 23: "Slow responses"

**Solutions:**
1. **Network latency**: OpenWeatherMap API might be slow
   - Add timeout to your code:
   ```python
   async with httpx.AsyncClient(timeout=30.0) as client:
   ```

2. **City with lots of data**: Try smaller city
3. **Overloaded server**: Try later, or get paid OpenWeatherMap plan

---

### Issue 24: "Timeout errors"

**Error:**
```
ReadTimeout
```

**Solutions:**
1. Increase timeout:
   ```python
   async with httpx.AsyncClient(timeout=15.0) as client:
   ```

2. Check internet connection

3. Check OpenWeatherMap API status

---

## General Debugging Tips

### Check FastAPI Terminal
Always check your FastAPI terminal when something breaks:
```
📍 Received request for city: Lahore, date: None
✅ Response sent: 🌤️ Current Weather in Lahore...
```

Or errors:
```
ERROR: ...
```

### Enable Debug Logging
Add to your `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test with curl
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

### Check OpenWeatherMap API Directly
```
https://api.openweathermap.org/data/2.5/weather?q=London&appid=ff09f16654861261ebb9d82eb601336e
```

If this works, your API key is valid.

---

## When All Else Fails

1. **Restart everything**:
   ```bash
   # Stop FastAPI: Ctrl+C
   # Stop ngrok: Ctrl+C
   # Kill any Python processes
   # Restart FastAPI: python main.py
   # Restart ngrok: ngrok http 8000
   ```

2. **Clear Dialogflow cache**:
   - Close Dialogflow
   - Clear browser cache
   - Reopen Dialogflow

3. **Check for typos**:
   - API key
   - Webhook URL
   - Parameter names
   - Intent names

4. **Start fresh**:
   - If too broken, create new Dialogflow agent
   - Recreate intents carefully
   - Test with new ngrok session

---

## Support Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- Dialogflow Docs: https://cloud.google.com/dialogflow/docs
- ngrok Docs: https://ngrok.com/docs
- OpenWeatherMap: https://openweathermap.org/api
- Python Docs: https://docs.python.org/3/

---

## Emergency Contacts

For InteractCX queries:
- Email: `candidatequeries@interactcx.com`

Good luck! You've got this! 💪
