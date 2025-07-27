from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
import os
import jwt
from typing import Optional

from rental_platform.services.property_service import PropertyService
from rental_platform.services.booking_service import BookingService

# Security
security = HTTPBearer()

# Supabase client
def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not supabase_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Supabase configuration missing"
        )
    
    return create_client(supabase_url, supabase_key)

# Property service dependency
def get_property_service(supabase_client: Client = Depends(get_supabase_client)) -> PropertyService:
    """Get property service instance"""
    return PropertyService(supabase_client)

# Booking service dependency
def get_booking_service(supabase_client: Client = Depends(get_supabase_client)) -> BookingService:
    """Get booking service instance"""
    return BookingService(supabase_client)

# Authentication
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase_client: Client = Depends(get_supabase_client)
) -> dict:
    """
    Get current authenticated user from JWT token
    """
    try:
        token = credentials.credentials
        
        # Verify token with Supabase
        response = supabase_client.auth.get_user(token)
        
        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Get user account information
        user_data = {
            "id": response.user.id,
            "email": response.user.email,
            "account_id": response.user.user_metadata.get("account_id", response.user.id)
        }
        
        return user_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

# Optional authentication (for public endpoints)
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    supabase_client: Client = Depends(get_supabase_client)
) -> Optional[dict]:
    """
    Get current user if authenticated, otherwise return None
    Used for endpoints that work with or without authentication
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials, supabase_client)
    except HTTPException:
        return None 