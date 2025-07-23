# Deploying to Heroku

This guide explains how to deploy the Flask Shop application to Heroku.

## Prerequisites

- Heroku account
- Heroku CLI installed
- Git repository setup

## Step 1: Login to Heroku

Use the Heroku CLI to log in:

```bash
heroku login
```

This will open a browser where you can authenticate.

## Step 2: Create a Heroku app (if not already created)

```bash
heroku create flask-shop-app
```

Or to use a specific name:

```bash
heroku create your-app-name
```

## Step 3: Add Heroku remote

```bash
heroku git:remote -a your-app-name
```

## Step 4: Configure Heroku for Python

Create/update the following files:

1. **.python-version** - Specifies Python version (just the major.minor like `3.10`)
2. **Procfile** - Tells Heroku how to run the application
3. **requirements.txt** - Lists all dependencies

## Step 5: Push to Heroku

```bash
git push heroku master
```

## Step 6: Set environment variables

```bash
heroku config:set SECRET_KEY=your_secret_key
heroku config:set FLASK_DEBUG=0
```

## Step 7: Open your application

```bash
heroku open
```

## Troubleshooting

Check logs if something goes wrong:

```bash
heroku logs --tail
```
