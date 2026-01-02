from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from models import MessageCreate, MessageResponse
from database import insert_message, get_all_messages

# Load environment variables
load_dotenv()

app = FastAPI(title="Contact Form API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Contact Form API is running"}


@app.get("/api/messages", response_model=list[MessageResponse])
async def get_messages():
    """Retrieve all submitted messages"""
    try:
        messages = get_all_messages()
        return messages
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error retrieving messages: {error_details}")  # Log to console
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {str(e)}")


@app.post("/api/messages", response_model=MessageResponse)
async def create_message(message: MessageCreate):
    """Submit a new contact form message"""
    try:
        result = insert_message(
            name=message.name,
            email=message.email,
            message=message.message
        )
        if not result:
            raise HTTPException(status_code=500, detail="Failed to insert message")
        return result
    except ValueError as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ValueError creating message: {error_details}")  # Log to console
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error creating message: {error_details}")  # Log to console
        raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/test-supabase")
async def test_supabase():
    """Test Supabase connection and configuration"""
    try:
        from database import get_supabase_client
        import os
        
        # Check environment variables
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        env_status = {
            "SUPABASE_URL": "✓ Set" if supabase_url else "✗ Missing",
            "SUPABASE_KEY": "✓ Set" if supabase_key else "✗ Missing"
        }
        
        # Try to connect
        if supabase_url and supabase_key:
            client = get_supabase_client()
            # Try a simple query to test connection
            result = client.table("messages").select("id").limit(1).execute()
            return {
                "status": "success",
                "environment": env_status,
                "connection": "✓ Connected",
                "table_exists": "✓ Table accessible"
            }
        else:
            return {
                "status": "error",
                "environment": env_status,
                "connection": "✗ Cannot connect - missing credentials"
            }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Test Supabase error: {error_details}")
        return {
            "status": "error",
            "error": str(e),
            "details": error_details
        }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

