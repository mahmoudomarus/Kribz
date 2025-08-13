"""
Property Agent Tools - Integrates with existing rental platform API
Located in correct path: backend/agent/tools/property_tools.py
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime, date

class PropertySearchTool:
    """Agent tool to search properties in the rental platform database"""
    
    def __init__(self, api_base_url: str = "https://kribz-i7jx.onrender.com/api/v1/rental"):
        self.api_base = api_base_url
    
    def search_properties(self, 
                         city: str = None,
                         property_type: str = None,  # "short_term" or "long_term"
                         min_price: float = None,
                         max_price: float = None,
                         bedrooms: int = None,
                         amenities: List[str] = None) -> Dict:
        """Search properties in the rental platform database"""
        
        params = {}
        if city: params['city'] = city
        if property_type: params['property_type'] = property_type
        if min_price: params['min_price'] = min_price
        if max_price: params['max_price'] = max_price
        if bedrooms: params['bedrooms'] = bedrooms
        if amenities: params['amenities'] = ','.join(amenities)
        
        try:
            response = requests.get(f"{self.api_base}/properties/search", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Could not search properties: {str(e)}"}

class PropertyBookingTool:
    """Agent tool to handle property bookings"""
    
    def __init__(self, api_base_url: str = "https://kribz-i7jx.onrender.com/api/v1/rental"):
        self.api_base = api_base_url
    
    def create_booking_request(self, property_id: str, booking_data: Dict, auth_token: str) -> Dict:
        """Create booking request through the rental platform"""
        
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/bookings/requests",
                json=booking_data,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Could not create booking: {str(e)}"}
