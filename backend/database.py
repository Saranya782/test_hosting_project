import os
from supabase import create_client, Client
from typing import List, Dict, Any


def get_supabase_client() -> Client:
    """Initialize and return Supabase client"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    
    # Clean up URL - remove trailing slash if present
    supabase_url = supabase_url.rstrip('/')
    
    # Validate URL format
    if not supabase_url.startswith('http://') and not supabase_url.startswith('https://'):
        raise ValueError(f"Invalid SUPABASE_URL format. URL must start with http:// or https://. Got: {supabase_url}")
    
    print(f"Attempting to connect to Supabase URL: {supabase_url}")  # Debug log
    
    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Failed to create Supabase client. URL: {supabase_url}, Error: {str(e)}")
        raise ValueError(f"Invalid Supabase URL or key: {str(e)}")


def insert_message(name: str, email: str, message: str) -> Dict[str, Any]:
    """Insert a new message into Supabase"""
    supabase = get_supabase_client()
    
    data = {
        "name": name,
        "email": email,
        "message": message
    }
    
    try:
        result = supabase.table("messages").insert(data).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Supabase insert error: {str(e)}")
        raise


def get_all_messages() -> List[Dict[str, Any]]:
    """Retrieve all messages from Supabase"""
    supabase = get_supabase_client()
    
    try:
        result = supabase.table("messages").select("*").order("created_at", desc=True).execute()
        return result.data if result.data else []
    except Exception as e:
        print(f"Supabase query error: {str(e)}")
        raise

