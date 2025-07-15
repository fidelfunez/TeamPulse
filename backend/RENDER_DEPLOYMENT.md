# Render Deployment Guide for TeamPulse Backend

## Prerequisites
- GitHub repository with your TeamPulse backend code
- Render account (free tier available)

## Step 1: Prepare Your Repository

Your backend is already properly configured for Render deployment with:
- ✅ `requirements.txt` with all dependencies including `gunicorn`
- ✅ `app.py` with proper Flask application factory
- ✅ `render.yaml` for automated deployment configuration
- ✅ Environment variables configured in `config.py`

## Step 2: Deploy to Render

### Option A: Using render.yaml (Recommended)
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Update the `CORS_ORIGINS` in `render.yaml` to match your Netlify frontend URL
6. Click "Apply" to deploy

### Option B: Manual Setup
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `teampulse-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

## Step 3: Configure Environment Variables

In your Render dashboard, go to your service → "Environment" tab and add:

### Required Variables:
```
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=https://your-netlify-site.netlify.app
FLASK_ENV=production
```

### Database Configuration:
Render will automatically provide a `DATABASE_URL` environment variable when you create a PostgreSQL database.

### Optional Variables:
```
JWT_ACCESS_TOKEN_EXPIRES=3600
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## Step 4: Set Up PostgreSQL Database

1. In your Render dashboard, go to "New +" → "PostgreSQL"
2. Name it `teampulse-db`
3. Choose the free plan
4. Copy the `DATABASE_URL` from the database dashboard
5. Add it to your web service's environment variables

## Step 5: Update Frontend Configuration

Once deployed, update your frontend's environment variables in Netlify:

1. Go to your Netlify dashboard
2. Navigate to Site settings → Environment variables
3. Update `VITE_API_URL` to your Render backend URL:
   ```
   VITE_API_URL=https://your-backend-name.onrender.com
   ```

## Step 6: Test the Deployment

1. Visit your Render backend URL (e.g., `https://teampulse-backend.onrender.com`)
2. You should see the API welcome message
3. Test the health endpoint: `https://your-backend-name.onrender.com/health`

## Troubleshooting

### Common Issues:

1. **Build fails**: Check that all dependencies are in `requirements.txt`
2. **Database connection fails**: Ensure `DATABASE_URL` is set correctly
3. **CORS errors**: Verify `CORS_ORIGINS` includes your frontend URL
4. **500 errors**: Check Render logs in the dashboard

### Checking Logs:
- Go to your Render service dashboard
- Click on "Logs" tab
- Look for any error messages during build or runtime

## Security Notes

- Render automatically generates HTTPS certificates
- Environment variables are encrypted at rest
- Free tier has some limitations but is sufficient for development

## Next Steps

After successful deployment:
1. Test all API endpoints
2. Update your frontend to use the new backend URL
3. Test the full application flow
4. Set up automatic deployments (happens automatically with Git integration)

Your backend will automatically redeploy whenever you push changes to your GitHub repository! 