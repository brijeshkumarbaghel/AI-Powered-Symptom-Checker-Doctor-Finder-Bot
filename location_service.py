"""
Location services for the Healthcare Assistant
Handles real-time location detection and nearby hospital finding
"""

import requests
import streamlit as st
import googlemaps
from geopy.geocoders import Nominatim
from typing import Optional, Tuple, List, Dict
import json
from config import GOOGLE_MAPS_API_KEY, IPINFO_API_KEY, DEFAULT_LOCATION, FACILITY_TYPES

class LocationService:
    """Service for handling location detection and nearby facility finding"""
    
    def __init__(self):
        self.gmaps_client = None
        if GOOGLE_MAPS_API_KEY:
            try:
                self.gmaps_client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
            except Exception as e:
                st.warning(f"Google Maps API not available: {e}")
        
        self.geocoder = Nominatim(user_agent="healthcare_assistant")
    
    def get_user_location_by_ip(self) -> Optional[Dict]:
        """Get user location using IP geolocation"""
        try:
            # Try with ipinfo.io first (more accurate)
            if IPINFO_API_KEY:
                response = requests.get(f'https://ipinfo.io/json?token={IPINFO_API_KEY}', timeout=5)
            else:
                response = requests.get('https://ipinfo.io/json', timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'loc' in data:
                    lat, lon = map(float, data['loc'].split(','))
                    return {
                        'lat': lat,
                        'lon': lon,
                        'city': data.get('city', 'Unknown'),
                        'region': data.get('region', 'Unknown'),
                        'country': data.get('country', 'Unknown')
                    }
        except Exception as e:
            st.warning(f"IP geolocation failed: {e}")
        
        # Fallback to a free service
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            if response.status_code == 200:
                ip_data = response.json()
                ip = ip_data['ip']
                
                # Get location from IP
                location_response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
                if location_response.status_code == 200:
                    location_data = location_response.json()
                    if location_data['status'] == 'success':
                        return {
                            'lat': location_data['lat'],
                            'lon': location_data['lon'],
                            'city': location_data['city'],
                            'region': location_data['regionName'],
                            'country': location_data['country']
                        }
        except Exception as e:
            st.warning(f"Fallback geolocation failed: {e}")
        
        return None
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """Convert address to coordinates"""
        try:
            location = self.geocoder.geocode(address)
            if location:
                return (location.latitude, location.longitude)
        except Exception as e:
            st.warning(f"Geocoding failed: {e}")
        return None
    
    def find_nearby_hospitals_real(self, lat: float, lon: float, radius_km: int = 10) -> List[Dict]:
        """Find real nearby hospitals using Google Places API"""
        hospitals = []
        
        if self.gmaps_client:
            try:
                # Search for hospitals
                places_result = self.gmaps_client.places_nearby(
                    location=(lat, lon),
                    radius=radius_km * 1000,  # Convert km to meters
                    type='hospital'
                )
                
                for place in places_result.get('results', []):
                    hospital_info = self._extract_place_info(place, lat, lon)
                    if hospital_info:
                        hospitals.append(hospital_info)
                
                # Also search for clinics
                clinics_result = self.gmaps_client.places_nearby(
                    location=(lat, lon),
                    radius=radius_km * 1000,
                    type='doctor'
                )
                
                for place in clinics_result.get('results', []):
                    clinic_info = self._extract_place_info(place, lat, lon, facility_type='Clinic')
                    if clinic_info:
                        hospitals.append(clinic_info)
                
            except Exception as e:
                st.error(f"Error accessing Google Places API: {e}")
                return self._get_fallback_hospitals(lat, lon, radius_km)
        
        else:
            # Use OpenStreetMap/Nominatim as fallback
            return self._search_osm_hospitals(lat, lon, radius_km)
        
        # Sort by distance
        hospitals.sort(key=lambda x: x['distance'])
        return hospitals[:15]  # Return top 15 results
    
    def _extract_place_info(self, place: Dict, user_lat: float, user_lon: float, facility_type: str = 'Hospital') -> Optional[Dict]:
        """Extract hospital information from Google Places result"""
        try:
            place_lat = place['geometry']['location']['lat']
            place_lon = place['geometry']['location']['lng']
            
            # Calculate distance
            distance = self._calculate_distance(user_lat, user_lon, place_lat, place_lon)
            
            # Get additional details
            place_id = place['place_id']
            details = None
            if self.gmaps_client:
                try:
                    details = self.gmaps_client.place(
                        place_id=place_id,
                        fields=['name', 'formatted_phone_number', 'website', 'opening_hours', 'rating']
                    )['result']
                except:
                    pass
            
            hospital_info = {
                'name': place.get('name', 'Unknown Hospital'),
                'type': facility_type,
                'distance': round(distance, 1),
                'rating': place.get('rating', 0) or (details.get('rating', 0) if details else 0),
                'address': place.get('vicinity', 'Address not available'),
                'lat': place_lat,
                'lon': place_lon,
                'place_id': place_id
            }
            
            if details:
                if 'formatted_phone_number' in details:
                    hospital_info['phone'] = details['formatted_phone_number']
                if 'website' in details:
                    hospital_info['website'] = details['website']
                if 'opening_hours' in details and 'weekday_text' in details['opening_hours']:
                    hospital_info['hours'] = '; '.join(details['opening_hours']['weekday_text'][:2])
            
            # Add specialties based on type
            if 'hospital' in place.get('types', []):
                hospital_info['specialties'] = ['Emergency Medicine', 'Internal Medicine', 'Surgery']
            else:
                hospital_info['specialties'] = ['General Practice', 'Primary Care']
            
            return hospital_info
            
        except Exception as e:
            st.warning(f"Error processing place data: {e}")
            return None
    
    def _search_osm_hospitals(self, lat: float, lon: float, radius_km: int) -> List[Dict]:
        """Search for hospitals using OpenStreetMap (Overpass API)"""
        hospitals = []
        
        try:
            # Overpass API query for hospitals
            overpass_url = "https://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json];
            (
              node["amenity"="hospital"](around:{radius_km * 1000},{lat},{lon});
              way["amenity"="hospital"](around:{radius_km * 1000},{lat},{lon});
              node["amenity"="clinic"](around:{radius_km * 1000},{lat},{lon});
              way["amenity"="clinic"](around:{radius_km * 1000},{lat},{lon});
            );
            out center;
            """
            
            response = requests.post(overpass_url, data=overpass_query, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                for element in data.get('elements', []):
                    if 'tags' in element:
                        tags = element['tags']
                        
                        # Get coordinates
                        if element['type'] == 'node':
                            elem_lat, elem_lon = element['lat'], element['lon']
                        elif 'center' in element:
                            elem_lat, elem_lon = element['center']['lat'], element['center']['lon']
                        else:
                            continue
                        
                        distance = self._calculate_distance(lat, lon, elem_lat, elem_lon)
                        
                        hospital_info = {
                            'name': tags.get('name', 'Unknown Medical Facility'),
                            'type': 'Hospital' if tags.get('amenity') == 'hospital' else 'Clinic',
                            'distance': round(distance, 1),
                            'rating': 4.0,  # Default rating for OSM data
                            'address': self._format_osm_address(tags),
                            'lat': elem_lat,
                            'lon': elem_lon,
                            'phone': tags.get('phone', 'Not available'),
                            'website': tags.get('website', ''),
                            'specialties': ['General Medicine']
                        }
                        
                        hospitals.append(hospital_info)
                        
        except Exception as e:
            st.warning(f"OpenStreetMap search failed: {e}")
            return self._get_fallback_hospitals(lat, lon, radius_km)
        
        hospitals.sort(key=lambda x: x['distance'])
        return hospitals[:15]
    
    def _format_osm_address(self, tags: Dict) -> str:
        """Format address from OSM tags"""
        address_parts = []
        
        for key in ['addr:housenumber', 'addr:street', 'addr:city', 'addr:state']:
            if key in tags:
                address_parts.append(tags[key])
        
        return ', '.join(address_parts) if address_parts else 'Address not available'
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        import math
        
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def _get_fallback_hospitals(self, lat: float, lon: float, radius_km: int) -> List[Dict]:
        """Fallback hospital data when APIs fail"""
        return [
            {
                "name": "General Hospital",
                "type": "Hospital", 
                "distance": 2.5,
                "rating": 4.2,
                "address": "Near your location",
                "phone": "Call for information",
                "specialties": ["Emergency Medicine", "General Medicine"],
                "lat": lat + 0.01,
                "lon": lon + 0.01
            },
            {
                "name": "Community Health Center",
                "type": "Clinic",
                "distance": 1.8,
                "rating": 4.0,
                "address": "Near your location", 
                "phone": "Call for information",
                "specialties": ["Primary Care", "Family Medicine"],
                "lat": lat - 0.01,
                "lon": lon - 0.01
            }
        ]
