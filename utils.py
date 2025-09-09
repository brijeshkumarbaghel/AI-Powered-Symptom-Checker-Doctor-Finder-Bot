"""
Utility functions for the Healthcare Assistant
"""

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import re


def validate_data_files():
    """Validate that required data files exist and are properly formatted"""
    required_files = ['DiseaseAndSymptoms.csv', 'Disease precaution.csv']
    missing_files = []
    
    for file in required_files:
        try:
            df = pd.read_csv(file)
            if df.empty:
                st.error(f"❌ {file} is empty")
                return False
        except FileNotFoundError:
            missing_files.append(file)
        except Exception as e:
            st.error(f"❌ Error reading {file}: {e}")
            return False
    
    if missing_files:
        st.error(f"❌ Missing required files: {', '.join(missing_files)}")
        st.info("Please ensure the following files are in your project directory:")
        for file in missing_files:
            st.write(f"• {file}")
        return False
    
    return True


def clean_symptom_text(symptom):
    """Clean and normalize symptom text"""
    if pd.isna(symptom) or not symptom:
        return ""
    
    # Convert to string and strip whitespace
    symptom = str(symptom).strip()
    
    # Replace underscores with spaces
    symptom = symptom.replace('_', ' ')
    
    # Remove extra whitespace
    symptom = ' '.join(symptom.split())
    
    # Convert to title case for display
    return symptom.title()


def format_disease_name(disease_name):
    """Format disease name for consistent display"""
    if pd.isna(disease_name) or not disease_name:
        return ""
    
    # Convert to string and strip
    disease_name = str(disease_name).strip()
    
    # Handle common abbreviations
    abbreviations = {
        'GERD': 'GERD (Gastroesophageal Reflux Disease)',
        'AIDS': 'AIDS (Acquired Immunodeficiency Syndrome)',
        'UTI': 'UTI (Urinary Tract Infection)'
    }
    
    return abbreviations.get(disease_name, disease_name)


def calculate_symptom_match_score(user_symptoms, disease_symptoms):
    """Calculate how well user symptoms match a disease"""
    if not user_symptoms or not disease_symptoms:
        return 0
    
    # Convert to sets for comparison
    user_set = set(symptom.lower().strip() for symptom in user_symptoms)
    disease_set = set(symptom.lower().strip() for symptom in disease_symptoms if symptom)
    
    # Calculate Jaccard similarity
    intersection = len(user_set.intersection(disease_set))
    union = len(user_set.union(disease_set))
    
    return intersection / union if union > 0 else 0


def generate_health_tips():
    """Generate general health tips"""
    tips = [
        "💧 Stay hydrated by drinking at least 8 glasses of water daily",
        "🏃‍♂️ Engage in regular physical activity for at least 30 minutes daily",
        "🥗 Maintain a balanced diet rich in fruits, vegetables, and whole grains",
        "😴 Get 7-9 hours of quality sleep each night",
        "🧘‍♀️ Practice stress management techniques like meditation or deep breathing",
        "🚭 Avoid smoking and limit alcohol consumption",
        "☀️ Get regular sunlight exposure for vitamin D synthesis",
        "🔍 Schedule regular health check-ups and screenings",
        "🧼 Maintain good hygiene practices, especially hand washing",
        "🤝 Stay socially connected with friends and family"
    ]
    return np.random.choice(tips, size=3, replace=False).tolist()


def format_confidence_score(score):
    """Format confidence score for display"""
    return f"{score:.1f}%"


def get_severity_color(confidence):
    """Get color based on confidence level"""
    if confidence >= 70:
        return "red"
    elif confidence >= 50:
        return "orange"
    elif confidence >= 30:
        return "yellow"
    else:
        return "green"


def create_symptom_severity_scale():
    """Create a symptom severity reference scale"""
    return {
        "Mild (1-3)": "Minor discomfort, doesn't interfere with daily activities",
        "Moderate (4-6)": "Noticeable symptoms, some interference with activities",
        "Severe (7-8)": "Significant symptoms, major interference with activities", 
        "Critical (9-10)": "Extreme symptoms, unable to perform normal activities"
    }


def log_user_interaction(feature_used, symptoms=None, location=None):
    """Log user interactions for analytics (in a real app, this would go to a database)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "feature": feature_used,
        "symptoms": symptoms,
        "location": location
    }
    
    # In a production app, you would save this to a database
    # For now, we'll just store it in session state
    if 'interaction_log' not in st.session_state:
        st.session_state.interaction_log = []
    
    st.session_state.interaction_log.append(log_entry)


def get_emergency_keywords():
    """Get keywords that indicate emergency situations"""
    return [
        'chest pain', 'difficulty breathing', 'shortness of breath', 'severe bleeding',
        'unconscious', 'fainting', 'severe headache', 'stroke', 'heart attack',
        'allergic reaction', 'severe pain', 'cannot breathe', 'choking',
        'severe burn', 'overdose', 'suicide', 'self harm', 'seizure'
    ]


def check_emergency_symptoms(symptom_text):
    """Check if symptoms indicate an emergency situation"""
    if not symptom_text:
        return False
    
    emergency_keywords = get_emergency_keywords()
    text_lower = symptom_text.lower()
    
    for keyword in emergency_keywords:
        if keyword in text_lower:
            return True
    
    return False


def format_medical_facility_info(facility):
    """Format medical facility information for display"""
    info = f"**{facility['name']}**\n"
    info += f"🏥 {facility['type']}\n"
    info += f"📍 {facility['address']}\n"
    info += f"⭐ {facility['rating']}/5.0\n"
    
    if 'phone' in facility:
        info += f"📞 {facility['phone']}\n"
    
    if 'hours' in facility:
        info += f"🕒 {facility['hours']}\n"
    
    if 'specialties' in facility:
        info += f"🩺 Specialties: {', '.join(facility['specialties'])}\n"
    
    return info


def generate_health_report(predictions, symptoms):
    """Generate a summary health report"""
    if not predictions or not symptoms:
        return ""
    
    report = "## 📋 Health Analysis Summary\n\n"
    report += f"**Analysis Date:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n"
    report += f"**Symptoms Analyzed:** {', '.join(symptoms)}\n\n"
    report += f"**Top Prediction:** {predictions[0]} (AI Analysis)\n\n"
    report += "**Recommendations:**\n"
    report += "• Consult with a healthcare provider for proper diagnosis\n"
    report += "• Monitor symptoms and seek immediate care if they worsen\n"
    report += "• Follow general health guidelines for recovery\n"
    report += "• Keep a record of symptoms for your healthcare provider\n\n"
    report += "**Disclaimer:** This analysis is for informational purposes only and should not replace professional medical advice.\n"
    
    return report


def create_symptom_timeline():
    """Create a template for symptom tracking"""
    timeline = {
        "date": [],
        "symptom": [],
        "severity": [],
        "duration": [],
        "notes": []
    }
    return timeline


def validate_location_input(location):
    """Validate location input"""
    if not location or len(location.strip()) < 3:
        return False, "Please enter a valid location (at least 3 characters)"
    
    # Basic validation - could be enhanced
    if re.match(r'^[a-zA-Z\s,.-]+$', location):
        return True, "Location format appears valid"
    
    return False, "Location contains invalid characters"


def format_distance(distance_km):
    """Format distance for display"""
    if distance_km < 1:
        return f"{distance_km * 1000:.0f} meters"
    elif distance_km < 10:
        return f"{distance_km:.1f} km"
    else:
        return f"{distance_km:.0f} km"


def get_facility_type_icon(facility_type):
    """Get appropriate icon for facility type"""
    icons = {
        "Hospital": "🏥",
        "Emergency": "🚑", 
        "Clinic": "🏥",
        "Family Medicine": "👨‍⚕️",
        "Specialist": "🩺",
        "Community Health": "🏥",
        "Pharmacy": "💊",
        "Urgent Care": "🚨"
    }
    return icons.get(facility_type, "🏥")


def create_export_data(analysis_results):
    """Create exportable data from analysis results"""
    export_data = {
        "timestamp": datetime.now().isoformat(),
        "analysis_type": "symptom_analysis",
        "results": analysis_results,
        "disclaimer": "This analysis is for informational purposes only. Consult healthcare providers for medical advice."
    }
    return export_data
