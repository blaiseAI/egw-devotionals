
# Devotional API

A FastAPI application that serves daily devotionals.

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

4. Access the API documentation at http://localhost:8000/docs

## API Endpoints

- GET `/`: Welcome message
- GET `/devotional`: Get today's devotional
- GET `/devotional?date=YYYY-MM-DD`: Get devotional for specific date
- GET `/health`: Health check endpoint

## Deployment

This application can be deployed to AWS Lambda using the provided handler.# egw-devotionals
