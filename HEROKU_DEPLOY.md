# Heroku Deployment Guide

This guide provides instructions for deploying this Flask application to Heroku.

## Files for Heroku Deployment

The following files are required for Heroku deployment:

1. `Procfile` - Tells Heroku how to run the application
   ```
   web: gunicorn app_direct:app --log-file - --bind 0.0.0.0:$PORT
   ```

2. `runtime.txt` - Specifies the Python version
   ```
   python-3.10.12
   ```

3. `requirements.txt` - Lists all required Python packages
   Heroku automatically installs packages from this file.

4. `app_direct.py` - The main Flask application file

## Deployment Steps

### Using Heroku Dashboard (Recommended)

1. Create a Heroku account at [heroku.com](https://heroku.com)
2. Create a new app in the Heroku dashboard
3. Go to the "Deploy" tab
4. Under "Deployment method" select "GitHub"
5. Connect to your GitHub repository
6. Select the branch to deploy (usually master)
7. Click "Deploy Branch"

### Using Heroku CLI

If the CLI works on your system:

```bash
# Login to Heroku
heroku login

# Add remote to git repository
heroku git:remote -a your-app-name

# Push to Heroku
git push heroku master
```

## Troubleshooting

- Check application logs: `heroku logs --tail`
- Ensure `app_direct.py` correctly handles the PORT environment variable
- Make sure all required packages are in requirements.txt
