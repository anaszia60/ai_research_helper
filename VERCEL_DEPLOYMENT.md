# 🚀 Vercel Deployment Guide for Research Co-Pilot

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be on GitHub
3. **Environment Variables**: Set up your API keys

## 🔧 Deployment Steps

### 1. Connect to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository: `anaszia60/ai_research_helper`
4. Select the repository

### 2. Configure Build Settings

- **Framework Preset**: Other
- **Build Command**: Leave empty (Vercel will auto-detect)
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

### 3. Set Environment Variables

In Vercel dashboard, add these environment variables:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Deploy

Click "Deploy" and wait for the build to complete.

## 🚨 Common Issues & Solutions

### Issue: 404 NOT_FOUND

**Cause**: Vercel can't find the entry point
**Solution**: 
1. Make sure `api/index.py` exists
2. Check that `vercel.json` is properly configured
3. Ensure the repository is connected correctly

### Issue: Build Failures

**Cause**: Python dependencies or version issues
**Solution**:
1. Check `requirements.txt` for compatibility
2. Verify Python version in `runtime.txt`
3. Check build logs for specific errors

### Issue: Environment Variables Not Working

**Cause**: API keys not set in Vercel
**Solution**:
1. Go to Project Settings → Environment Variables
2. Add `GEMINI_API_KEY` with your actual key
3. Redeploy the project

## 🔍 Troubleshooting Steps

### 1. Check Build Logs

In Vercel dashboard:
1. Go to your project
2. Click on the latest deployment
3. Check "Build Logs" for errors

### 2. Verify File Structure

Your repository should have:
```
ai_research_helper/
├── api/
│   └── index.py          # Vercel entry point
├── co_pilot_web.py       # Flask app
├── research_co_pilot.py  # Core logic
├── templates/
│   └── co_pilot.html     # Web interface
├── vercel.json           # Vercel config
├── requirements.txt      # Dependencies
└── runtime.txt           # Python version
```

### 3. Test Locally First

Before deploying to Vercel:
```bash
# Test the Flask app locally
python3 co_pilot_web.py

# Test the API entry point
python3 api/index.py
```

## 🎯 Alternative Deployment Options

### Option 1: Render.com
- Free tier available
- Better Python support
- Easier Flask deployment

### Option 2: Railway.app
- Simple deployment
- Good Python support
- Free tier available

### Option 3: Heroku
- Classic Python hosting
- Free tier discontinued
- Good for production

## 📱 After Successful Deployment

1. **Test the API endpoints**:
   - `GET /` - Main page
   - `POST /api/initialize` - Initialize system
   - `POST /api/step1_topic` - Topic refinement

2. **Check environment variables** are working

3. **Monitor performance** and logs

4. **Share your deployed URL** with others

## 🆘 Getting Help

If you still get errors:

1. **Check Vercel build logs** for specific error messages
2. **Verify all files** are in the repository
3. **Test locally** to ensure code works
4. **Check Vercel documentation** for Python apps
5. **Create an issue** in your GitHub repository

## 🔄 Redeployment

After making changes:
1. Push to GitHub
2. Vercel will auto-deploy
3. Or manually trigger deployment in Vercel dashboard

---

**Happy Deploying! 🚀**

Your Research Co-Pilot will be accessible worldwide once deployed successfully!
