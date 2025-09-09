"""
Configuration settings for the Healthcare Assistant
"""

import os

# Application Settings
APP_TITLE = "Intelligent Healthcare Assistant"
APP_ICON = "🏥"
VERSION = "1.0.0"

# File Paths
DATA_DIR = "."
DISEASES_FILE = os.path.join(DATA_DIR, "DiseaseAndSymptoms.csv")
PRECAUTIONS_FILE = os.path.join(DATA_DIR, "Disease precaution.csv")

# ML Model Settings
MODEL_CONFIDENCE_THRESHOLD = 0.01  # Minimum confidence for predictions
TOP_PREDICTIONS = 5  # Number of top predictions to show
RANDOM_STATE = 42

# Location Services
DEFAULT_SEARCH_RADIUS = 10  # km
MAX_SEARCH_RADIUS = 50  # km
GEOCODER_USER_AGENT = "healthcare_assistant_v1.0"

# Google Maps API Configuration
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

# IP Geolocation API Configuration
IPINFO_API_KEY = os.getenv('IPINFO_API_KEY', '')

# Default location if geolocation fails
DEFAULT_LOCATION = {
    'city': 'New York',
    'state': 'NY', 
    'country': 'US',
    'lat': 40.7128,
    'lon': -74.0060
}

# Healthcare facility types to search for
FACILITY_TYPES = [
    'hospital',
    'doctor',
    'pharmacy',
    'dentist',
    'physiotherapist'
]

# UI Settings
MAX_SYMPTOMS_DISPLAY = 10
MAP_HEIGHT = 500
DEFAULT_MAP_ZOOM = 12

# Emergency Contacts (US - modify for your location)
EMERGENCY_CONTACTS = {
    "Emergency Services": "911",
    "Poison Control": "1-800-222-1222",
    "Mental Health Crisis": "988",
    "Non-Emergency Medical": "311"
}

# Mock Doctor Data (for demonstration)
# In a real application, this would be replaced with API calls
MOCK_DOCTORS = [
    {
        "name": "City General Hospital",
        "type": "Hospital",
        "specialties": ["Emergency Medicine", "Internal Medicine", "Surgery"],
        "rating": 4.2,
        "address": "123 Medical Center Drive",
        "phone": "(555) 123-4567",
        "hours": "24/7",
        "accepts_emergency": True
    },
    {
        "name": "Dr. Sarah Johnson Family Clinic",
        "type": "Family Medicine",
        "specialties": ["Family Medicine", "Pediatrics"],
        "rating": 4.5,
        "address": "456 Health Avenue",
        "phone": "(555) 234-5678",
        "hours": "Mon-Fri 8:00 AM - 6:00 PM",
        "accepts_emergency": False
    },
    {
        "name": "Emergency Care Center",
        "type": "Emergency",
        "specialties": ["Emergency Medicine", "Urgent Care"],
        "rating": 4.0,
        "address": "789 Emergency Boulevard",
        "phone": "(555) 345-6789",
        "hours": "24/7",
        "accepts_emergency": True
    },
    {
        "name": "Specialty Medical Group",
        "type": "Specialist",
        "specialties": ["Cardiology", "Neurology", "Orthopedics"],
        "rating": 4.3,
        "address": "321 Specialist Way",
        "phone": "(555) 456-7890",
        "hours": "Mon-Fri 9:00 AM - 5:00 PM",
        "accepts_emergency": False
    },
    {
        "name": "Community Health Clinic",
        "type": "Community Health",
        "specialties": ["General Medicine", "Preventive Care"],
        "rating": 4.1,
        "address": "654 Community Street",
        "phone": "(555) 567-8901",
        "hours": "Mon-Sat 7:00 AM - 7:00 PM",
        "accepts_emergency": False
    }
]

# Warning Messages
EMERGENCY_WARNING = """
🚨 **EMERGENCY SITUATIONS** 🚨

If you're experiencing any of the following, call emergency services (911) immediately:
• Chest pain or pressure
• Difficulty breathing or shortness of breath
• Severe bleeding that won't stop
• Loss of consciousness or fainting
• Signs of stroke (sudden confusion, trouble speaking, severe headache)
• Severe allergic reactions
• Thoughts of self-harm or suicide
• Severe injuries from accidents

This tool is for informational purposes only and should never delay emergency medical care.
"""

MEDICAL_DISCLAIMER = """
⚠️ **IMPORTANT MEDICAL DISCLAIMER**

This healthcare assistant provides information based on AI analysis of your symptoms. However:

• This tool is NOT a substitute for professional medical advice
• Always consult with qualified healthcare providers for proper diagnosis
• AI predictions may not account for all medical conditions or personal factors
• Do not use this tool to self-diagnose or avoid seeking medical care
• If symptoms persist or worsen, contact a healthcare provider immediately

The creators of this tool are not responsible for any medical decisions made based on this information.
"""
