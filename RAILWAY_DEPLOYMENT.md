# Railway Deployment Guide

## ✅ Prerequisites Checklist

Your project is now fully configured for Railway deployment with:
- ✓ `requirements.txt` - All Python dependencies
- ✓ `Procfile` - Process configuration
- ✓ `runtime.txt` - Python version specification
- ✓ `railway.json` - Railway-specific configuration
- ✓ `main.py` - FastAPI app with CORS and health check
- ✓ Git repository initialized

## 🚀 Deploy to Railway

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Deploy on Railway

1. Go to [Railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your `vedic-astrology-api` repository
6. Railway will automatically detect your Procfile and deploy

### Step 3: Monitor Deployment

Railway will:
- ✓ Detect Python from `runtime.txt`
- ✓ Install dependencies from `requirements.txt`
- ✓ Run the start command from `Procfile`
- ✓ Assign a public URL (e.g., `https://yourapp.railway.app`)

### Step 4: Access Your API

Once deployed, your API will be available at:
```
https://your-app-name.railway.app
```

**Endpoints:**
- Health Check: `GET https://your-app-name.railway.app/`
- API Docs: `GET https://your-app-name.railway.app/docs`
- Birth Chart: `POST https://your-app-name.railway.app/birth_chart`

## 🔍 Testing Your Deployed API

### Test Health Endpoint
```bash
curl https://your-app-name.railway.app/
```

### Test Birth Chart Endpoint
```bash
curl -X POST https://your-app-name.railway.app/birth_chart \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "date": "15th January, 1990",
    "time": "10:30 AM",
    "place": "New York, USA"
  }'
```

## 🛠️ Environment Variables (Optional)

If you need to add environment variables:
1. Go to your Railway project dashboard
2. Click on your service
3. Go to "Variables" tab
4. Add any required variables

## 📊 Monitoring

Railway provides:
- **Logs**: Real-time application logs
- **Metrics**: CPU, Memory usage
- **Deployments**: History of all deployments
- **Health Checks**: Automatic monitoring via `/` endpoint

## ⚠️ Important Notes

1. **Free Tier**: Railway offers $5 free credit per month
2. **Cold Starts**: Free tier apps may sleep after inactivity
3. **Geocoding**: The app uses Nominatim (may have rate limits)
4. **CORS**: Currently set to `allow_origins=["*"]` - restrict this in production

## 🔄 Updating Your App

To deploy updates:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Railway will automatically redeploy!

## 🐛 Troubleshooting

### If deployment fails:
1. Check Railway logs in the dashboard
2. Verify Python version compatibility
3. Ensure all dependencies in `requirements.txt` are compatible

### Common issues:
- **Port binding**: Don't hardcode ports, use `$PORT` environment variable
- **Missing dependencies**: All packages must be in `requirements.txt`
- **Timeout**: First deployment may take 5-10 minutes

## 📖 Additional Resources

- [Railway Docs](https://docs.railway.app)
- [Railway Community](https://help.railway.app)
- [FastAPI on Railway](https://railway.app/starters/fastapi)
