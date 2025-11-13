import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents
from schemas import Interest, MediaItem, EventEntry

app = FastAPI(title="Cluster 1 Youth for Christ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Cluster 1 Youth for Christ API is running"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# -------------------- Interest (Sign-ups) --------------------
class InterestCreate(Interest):
    pass

class InterestPublic(BaseModel):
    id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    age: Optional[int] = None
    preferred_ministry: Optional[str] = None
    message: Optional[str] = None

@app.post("/api/interests", response_model=dict)
def create_interest(payload: InterestCreate):
    try:
        inserted_id = create_document("interest", payload)
        return {"id": inserted_id, "message": "Thanks for reaching out! We'll connect with you soon."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/interests", response_model=List[InterestPublic])
def list_interests(limit: int = 50):
    try:
        docs = get_documents("interest", limit=limit)
        result: List[InterestPublic] = []
        for d in docs:
            result.append(InterestPublic(
                id=str(d.get("_id")),
                full_name=d.get("full_name"),
                email=d.get("email"),
                phone=d.get("phone"),
                age=d.get("age"),
                preferred_ministry=d.get("preferred_ministry"),
                message=d.get("message"),
            ))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- Media (Photos/Videos) --------------------
class MediaCreate(MediaItem):
    pass

class MediaPublic(BaseModel):
    id: str
    kind: str
    url: str
    caption: Optional[str] = None
    taken_at: Optional[str] = None

@app.post("/api/media", response_model=dict)
def create_media(payload: MediaCreate):
    try:
        inserted_id = create_document("mediaitem", payload)
        return {"id": inserted_id, "message": "Media saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/media", response_model=List[MediaPublic])
def list_media(limit: int = 50):
    try:
        docs = get_documents("mediaitem", limit=limit)
        items: List[MediaPublic] = []
        for d in docs:
            items.append(MediaPublic(
                id=str(d.get("_id")),
                kind=d.get("kind"),
                url=str(d.get("url")),
                caption=d.get("caption"),
                taken_at=d.get("taken_at"),
            ))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- Events (Past Events) --------------------
class EventCreate(EventEntry):
    pass

class EventPublic(BaseModel):
    id: str
    title: str
    date: str
    location: Optional[str] = None
    description: Optional[str] = None
    photos: Optional[List[str]] = None
    video: Optional[str] = None

@app.post("/api/events", response_model=dict)
def create_event(payload: EventCreate):
    try:
        inserted_id = create_document("evententry", payload)
        return {"id": inserted_id, "message": "Event saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/events", response_model=List[EventPublic])
def list_events(limit: int = 50):
    try:
        docs = get_documents("evententry", limit=limit)
        items: List[EventPublic] = []
        for d in docs:
            items.append(EventPublic(
                id=str(d.get("_id")),
                title=d.get("title"),
                date=d.get("date"),
                location=d.get("location"),
                description=d.get("description"),
                photos=[str(p) for p in (d.get("photos") or [])],
                video=str(d.get("video")) if d.get("video") else None,
            ))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
