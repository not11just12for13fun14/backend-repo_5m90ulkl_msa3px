import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import create_document, get_documents
from schemas import Interest

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

# Models for request/response
class InterestCreate(Interest):
    pass

class InterestPublic(BaseModel):
    id: str
    full_name: str
    email: str
    phone: str | None
    age: int | None
    preferred_ministry: str | None
    message: str | None

# Endpoints for interest sign-ups
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
