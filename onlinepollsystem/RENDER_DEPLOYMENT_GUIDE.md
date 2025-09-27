# Deploying Django Online Poll System to Render

This guide will walk you through deploying your Django REST API to Render, a modern cloud platform that makes deployment simple and reliable.

## Prerequisites

1. A GitHub account with your code pushed to a repository
2. A Render account (free tier available at https://render.com)
3. Your Django project with all the configuration files we've created

## Step 1: Prepare Your Repository

### 1.1 Ensure all files are in your repository:
```bash
# Make sure you're in the project directory
cd /home/favour/ALX_PDBE/alx-project-nexus/onlinepollsystem

# Add all files to git
git add .

# Commit the changes
git commit -m "Add Render deployment configuration"

# Push to GitHub
git push origin main
```

### 1.2 Verify these files exist in your repository:
- ✅ `render.yaml` - Render deployment configuration
- ✅ `build.sh` - Build script for deployment
- ✅ `requirements.txt` - Python dependencies (updated with render packages)
- ✅ `manage.py` - Django management script
- ✅ Updated `settings.py` with Render configuration

## Step 2: Create Render Account and Connect Repository

### 2.1 Sign up for Render:
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up using your GitHub account (recommended)
4. Verify your email address

### 2.2 Connect Your GitHub Repository:
1. In Render dashboard, click "New +" button
2. Select "Blueprint" 
3. Connect your GitHub account if not already connected
4. Select your repository: `alx-project-nexus`
5. Give your blueprint a name: `onlinepollsystem-api`

## Step 3: Configure Environment Variables

Render will automatically detect the `render.yaml` file, but you may need to set additional environment variables:

### 3.1 Required Environment Variables:
```
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=false
DJANGO_SETTINGS_MODULE=onlinepollsystem.settings
```

### 3.2 Optional Environment Variables:
```
WEB_CONCURRENCY=4
PYTHON_VERSION=3.10.12
```

## Step 4: Deploy Your Application

### 4.1 Start Deployment:
1. After connecting the repository, Render will show the blueprint preview
2. Review the services that will be created:
   - Web Service: `onlinepollsystem-api`
   - PostgreSQL Database: `onlinepollsystem-db`
3. Click "Apply" to start the deployment

### 4.2 Monitor the Build Process:
1. Render will start building your application
2. You can monitor the build logs in real-time
3. The build process will:
   - Install Python dependencies
   - Run database migrations
   - Collect static files
   - Start the web server

## Step 5: Verify Deployment

### 5.1 Check Service Status:
1. Go to your Render dashboard
2. You should see two services:
   - ✅ `onlinepollsystem-api` (Web Service)
   - ✅ `onlinepollsystem-db` (PostgreSQL Database)

### 5.2 Test Your API:
1. Click on your web service to get the URL
2. Your API will be available at: `https://your-service-name.onrender.com`
3. Test the API endpoints:
   - Health check: `https://your-app.onrender.com/admin/` (Django admin)
   - API documentation: `https://your-app.onrender.com/swagger/`
   - API root: `https://your-app.onrender.com/api/`

## Step 6: API Endpoints Available

Once deployed, your Online Poll System API will have these endpoints:

### Authentication Endpoints:
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/token/refresh/` - JWT token refresh

### Polls Endpoints:
- `GET /api/polls/` - List all polls
- `POST /api/polls/` - Create new poll
- `GET /api/polls/{id}/` - Get specific poll
- `PUT /api/polls/{id}/` - Update poll
- `DELETE /api/polls/{id}/` - Delete poll

### Voting Endpoints:
- `POST /api/votes/` - Cast a vote
- `GET /api/votes/` - List user's votes

### API Documentation:
- `GET /swagger/` - Swagger UI documentation
- `GET /redoc/` - ReDoc documentation

## Step 7: Post-Deployment Configuration

### 7.1 Create Superuser (Optional):
To access Django admin, you'll need to create a superuser:
1. Go to your Render dashboard
2. Click on your web service
3. Go to "Shell" tab
4. Run: `python manage.py createsuperuser`
5. Follow the prompts to create an admin user

### 7.2 Monitor Your Application:
- **Logs**: Check service logs for any errors
- **Metrics**: Monitor CPU and memory usage
- **Database**: Monitor database connections and queries

## Step 8: Custom Domain (Optional)

### 8.1 Add Custom Domain:
1. Go to your web service settings
2. Click "Custom Domains"
3. Add your domain name
4. Follow DNS configuration instructions

## Troubleshooting Common Issues

### Issue 1: Build Failures
**Problem**: Build fails with dependency errors
**Solution**: 
- Check `requirements.txt` for correct package versions
- Ensure all dependencies are compatible
- Check build logs for specific error messages

### Issue 2: Database Connection Errors
**Problem**: Cannot connect to PostgreSQL database
**Solution**:
- Verify `DATABASE_URL` environment variable is set
- Check that database service is running
- Ensure `dj-database-url` is in requirements.txt

### Issue 3: Static Files Not Loading
**Problem**: CSS/JS files return 404 errors
**Solution**:
- Verify `whitenoise` is installed and configured
- Check that `collectstatic` runs during build
- Ensure `STATIC_ROOT` is correctly set

### Issue 4: CORS Errors (if using frontend)
**Problem**: Frontend cannot access API due to CORS
**Solution**:
- Install `django-cors-headers`
- Configure CORS settings in `settings.py`
- Add frontend domain to `CORS_ALLOWED_ORIGINS`

## Costs and Limitations

### Free Tier Limits:
- **Web Service**: 750 hours/month (enough for one always-on service)
- **PostgreSQL**: 1GB storage, 100 connections
- **Bandwidth**: 100GB/month
- **Build Minutes**: 500 minutes/month

### Paid Plans:
- **Web Service**: Starting at $7/month for always-on services
- **PostgreSQL**: Starting at $7/month for 1GB+ storage
- **Professional features**: Custom domains, advanced metrics, priority support

## Next Steps

1. **Security**: Change default `SECRET_KEY` to a secure random key
2. **Monitoring**: Set up error tracking (Sentry, Rollbar)
3. **Caching**: Add Redis for caching if needed
4. **CDN**: Use a CDN for better static file performance
5. **Backups**: Set up regular database backups
6. **CI/CD**: Set up automated testing before deployment

## Support and Resources

- **Render Documentation**: https://render.com/docs
- **Django Deployment Guide**: https://docs.djangoproject.com/en/stable/howto/deployment/
- **Community**: Render Discord/Forum for support
- **Status Page**: https://status.render.com for service status

---

Your Django Online Poll System is now deployed and accessible worldwide! 🚀

The API will automatically restart when you push changes to your GitHub repository, making updates seamless.