from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from mangum import Mangum
from typing import Optional
from pydantic import BaseModel
from devotional_scraper import DevotionalScraper

app = FastAPI(
    title="Devotional API",
    description="API for fetching daily devotionals",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scraper
scraper = DevotionalScraper()

class DevotionalResponse(BaseModel):
    date: str
    title: str
    subtitle: str
    verse: str
    content: str
    thought_for_day: str
    source: str
    url: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Devotional API"}

@app.get("/devotional", response_model=DevotionalResponse)
async def get_devotional(date: Optional[str] = None):
    try:
        if date:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        else:
            date_obj = datetime.now()
        
        devotional = scraper.get_devotional(date_obj)
        
        if not devotional:
            raise HTTPException(status_code=404, detail="Devotional not found")
            
        return devotional
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Handler for AWS Lambda
handler = Mangum(app)