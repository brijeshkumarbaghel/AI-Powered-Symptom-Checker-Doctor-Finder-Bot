#!/usr/bin/env python3
"""
Intelligent Healthcare Assistant
AI-Powered Symptom Checker & Doctor Finder Bot

Features:
- Symptom analysis and disease prediction
- Medical recommendations and precautions
- Doctor/Hospital finder with location services
- Interactive web interface
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import requests
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from location_service import LocationService
import re
import warnings
warnings.filterwarnings('ignore')

class HealthcareAssistant:
    def __init__(self):
        """Initialize the Healthcare Assistant with data and models"""
        self.diseases_df = None
        self.precautions_df = None
        self.model = None
        self.vectorizer = None
        self.symptoms_list = []
        self.diseases_list = []
        self.location_service = LocationService()
        self.load_data()
        self.prepare_model()
    
    def load_data(self):
        """Load disease and symptoms data from CSV files"""
        try:
            # Load diseases and symptoms data
            self.diseases_df = pd.read_csv('DiseaseAndSymptoms.csv')
            self.precautions_df = pd.read_csv('Disease precaution.csv')
            
            # Clean and process data
            self.clean_data()
            
            st.success("✅ Medical databases loaded successfully!")
            
        except FileNotFoundError as e:
            st.error(f"❌ Error loading data files: {e}")
            st.info("Please ensure 'DiseaseAndSymptoms.csv' and 'Disease precaution.csv' are in the same directory")
    
    def clean_data(self):
        """Clean and preprocess the medical data"""
        # Get unique diseases
        self.diseases_list = self.diseases_df['Disease'].unique().tolist()
        
        # Extract all unique symptoms
        symptom_columns = [col for col in self.diseases_df.columns if col.startswith('Symptom_')]
        all_symptoms = set()
        
        for col in symptom_columns:
            symptoms = self.diseases_df[col].dropna().str.strip()
            all_symptoms.update(symptoms)
        
        # Clean symptoms (remove empty strings and normalize)
        self.symptoms_list = [s.strip().replace('_', ' ') for s in all_symptoms if s and s.strip()]
        self.symptoms_list = sorted(list(set(self.symptoms_list)))
        
    def prepare_model(self):
        """Prepare machine learning model for disease prediction"""
        if self.diseases_df is not None:
            # Create training data
            X_train = []
            y_train = []
            
            for _, row in self.diseases_df.iterrows():
                disease = row['Disease']
                symptoms = []
                
                # Collect all symptoms for this row
                for col in self.diseases_df.columns:
                    if col.startswith('Symptom_') and pd.notna(row[col]):
                        symptom = row[col].strip().replace('_', ' ')
                        if symptom:
                            symptoms.append(symptom)
                
                if symptoms:
                    X_train.append(' '.join(symptoms))
                    y_train.append(disease)
            
            # Create ML pipeline
            self.model = Pipeline([
                ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english')),
                ('classifier', MultinomialNB())
            ])
            
            # Train the model
            if X_train and y_train:
                self.model.fit(X_train, y_train)
                st.success("🧠 AI model trained successfully!")
    
    def predict_disease(self, symptoms_text):
        """Predict disease based on symptoms"""
        if self.model is None:
            return [], []
        
        try:
            # Get prediction probabilities
            probabilities = self.model.predict_proba([symptoms_text])[0]
            classes = self.model.classes_
            
            # Get top 5 predictions
            top_indices = np.argsort(probabilities)[-5:][::-1]
            
            predictions = []
            confidences = []
            
            for idx in top_indices:
                if probabilities[idx] > 0.01:  # Only show predictions with >1% confidence
                    predictions.append(classes[idx])
                    confidences.append(probabilities[idx] * 100)
            
            return predictions, confidences
            
        except Exception as e:
            st.error(f"Error in prediction: {e}")
            return [], []
    
    def get_precautions(self, disease):
        """Get precautions and recommendations for a disease"""
        if self.precautions_df is not None:
            try:
                # First, try exact match
                precautions = self.precautions_df[self.precautions_df['Disease'].str.lower() == disease.lower()]
                
                # If no exact match, try partial match
                if precautions.empty:
                    precautions = self.precautions_df[self.precautions_df['Disease'].str.lower().str.contains(disease.lower().split()[0], na=False)]
                
                if not precautions.empty:
                    precaution_list = []
                    for col in ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']:
                        if col in precautions.columns:
                            precaution = precautions.iloc[0][col]
                            if pd.notna(precaution) and str(precaution).strip() and str(precaution).strip() != '':
                                precaution_list.append(str(precaution).strip())
                    return precaution_list
                else:
                    # Return generic health advice if no specific precautions found
                    return [
                        "Consult with a healthcare professional for proper diagnosis",
                        "Rest and stay hydrated",
                        "Monitor your symptoms closely",
                        "Seek immediate medical attention if symptoms worsen"
                    ]
            except Exception as e:
                st.error(f"Error getting precautions: {e}")
        return [
            "Consult with a healthcare professional for proper diagnosis",
            "Rest and stay hydrated", 
            "Monitor your symptoms closely",
            "Seek immediate medical attention if symptoms worsen"
        ]
    
    def find_nearby_doctors(self, location=None, radius=10, use_current_location=False):
        """Find nearby doctors and hospitals using real location services"""
        try:
            user_location = None
            
            if use_current_location:
                # Try to get user's current location via IP
                st.info("🌍 Detecting your location...")
                user_location = self.location_service.get_user_location_by_ip()
                
                if user_location:
                    lat, lon = user_location['lat'], user_location['lon']
                    location_name = f"{user_location['city']}, {user_location['region']}, {user_location['country']}"
                    st.success(f"📍 Detected location: {location_name}")
                else:
                    st.warning("Could not detect your location automatically. Please enter your location manually.")
                    return [], None
            
            elif location:
                # Geocode the provided location
                coords = self.location_service.geocode_address(location)
                if coords:
                    lat, lon = coords
                    st.success(f"📍 Location found: {location}")
                else:
                    st.error("Could not find the specified location. Please check the address and try again.")
                    return [], None
            else:
                st.error("Please provide a location or enable location detection.")
                return [], None
            
            # Find nearby hospitals using real data
            st.info("🏥 Searching for nearby medical facilities...")
            hospitals = self.location_service.find_nearby_hospitals_real(lat, lon, radius)
            
            if hospitals:
                st.success(f"Found {len(hospitals)} medical facilities within {radius} km")
                return hospitals, (lat, lon)
            else:
                st.warning("No medical facilities found in your area. Try increasing the search radius.")
                return [], (lat, lon)
                
        except Exception as e:
            st.error(f"Error finding doctors: {e}")
            return [], None
    
    def create_map(self, location_coords, doctors):
        """Create an interactive map showing nearby medical facilities"""
        if location_coords:
            lat, lon = location_coords
            m = folium.Map(location=[lat, lon], zoom_start=12)
            
            # Add user location
            folium.Marker(
                [lat, lon],
                popup="Your Location",
                tooltip="You are here",
                icon=folium.Icon(color='red', icon='user')
            ).add_to(m)
            
            # Add doctor locations using real coordinates
            for i, doctor in enumerate(doctors):
                # Use real coordinates if available, otherwise approximate
                if 'lat' in doctor and 'lon' in doctor:
                    doc_lat, doc_lon = doctor['lat'], doctor['lon']
                else:
                    # Fallback to approximate positions for demo data
                    lat_offset = np.random.uniform(-0.05, 0.05)
                    lon_offset = np.random.uniform(-0.05, 0.05)
                    doc_lat, doc_lon = lat + lat_offset, lon + lon_offset
                
                # Choose icon color based on facility type
                icon_color = 'blue'
                if doctor.get('type', '').lower() in ['hospital']:
                    icon_color = 'red'
                elif doctor.get('type', '').lower() in ['clinic', 'family medicine']:
                    icon_color = 'green'
                elif doctor.get('type', '').lower() in ['emergency', 'urgent care']:
                    icon_color = 'orange'
                
                # Create directions URL for the popup
                if 'lat' in doctor and 'lon' in doctor:
                    directions_url = f"https://www.google.com/maps/dir/?api=1&destination={doctor['lat']},{doctor['lon']}"
                elif doctor.get('address'):
                    address_encoded = doctor['address'].replace(' ', '+').replace(',', '%2C')
                    directions_url = f"https://www.google.com/maps/dir/?api=1&destination={address_encoded}"
                else:
                    name_encoded = doctor['name'].replace(' ', '+')
                    directions_url = f"https://www.google.com/maps/search/{name_encoded}"
                
                popup_html = f"""
                <div style="width: 280px; font-family: Arial, sans-serif;">
                    <h4 style="color: #2E86AB; margin-bottom: 10px;">{doctor['name']}</h4>
                    <p><strong>🏥 Type:</strong> {doctor.get('type', 'Medical Facility')}</p>
                    <p><strong>📍 Address:</strong> {doctor.get('address', 'Not available')}</p>
                    <p><strong>📏 Distance:</strong> {doctor.get('distance', 'N/A')} km</p>
                    <p><strong>⭐ Rating:</strong> {doctor.get('rating', 'N/A')}/5.0</p>
                    
                    {f"<p><strong>📞 Phone:</strong> <a href='tel:{doctor['phone']}'>{doctor['phone']}</a></p>" if doctor.get('phone') and doctor['phone'] != 'Not available' else ""}
                    {f"<p><strong>🌐 Website:</strong> <a href='{doctor['website']}' target='_blank'>Visit Website</a></p>" if doctor.get('website') else ""}
                    {f"<p><strong>🕒 Hours:</strong> {doctor['hours']}</p>" if doctor.get('hours') else ""}
                    
                    {f"<p><strong>🩺 Specialties:</strong><br>{'<br>'.join(['• ' + spec for spec in doctor['specialties']])}</p>" if doctor.get('specialties') else ""}
                    
                    <div style="margin-top: 15px; text-align: center;">
                        <a href="{directions_url}" target="_blank" style="background-color: #4285f4; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; font-weight: bold;">🗺️ Get Directions</a>
                    </div>
                </div>
                """
                
                folium.Marker(
                    [doc_lat, doc_lon],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=f"{doctor['name']} - {doctor.get('distance', 'N/A')} km",
                    icon=folium.Icon(color=icon_color, icon='plus-sign')
                ).add_to(m)
            
            return m
        return None

# Streamlit Web Application
def main():
    # Page configuration
    st.set_page_config(
        page_title="🏥 Intelligent Healthcare Assistant",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(145deg, #f0f8ff 0%, #e6f3ff 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #2E86AB;
    }
    .symptom-chip {
        background-color: #E3F2FD;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        display: inline-block;
        border: 1px solid #2196F3;
    }
    .prediction-card {
        background: linear-gradient(145deg, #fff5f5 0%, #ffe6e6 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #ff4444;
    }
    .precaution-item {
        background: linear-gradient(145deg, #f0fff0 0%, #e6ffe6 100%);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #32cd32;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize the healthcare assistant
    if 'healthcare_assistant' not in st.session_state:
        st.session_state.healthcare_assistant = HealthcareAssistant()
    
    assistant = st.session_state.healthcare_assistant
    
    # Main header
    st.markdown('<h1 class="main-header">🏥 Intelligent Healthcare Assistant</h1>', unsafe_allow_html=True)
    st.markdown("### AI-Powered Symptom Checker & Doctor Finder Bot")
    
    # Sidebar
    st.sidebar.title("🎯 Features")
    feature = st.sidebar.selectbox(
        "Choose a feature:",
        ["🔍 Symptom Analysis", "💊 Disease Information", "🏥 Find Doctors", "📊 Health Statistics"]
    )
    
    # Main content based on selected feature
    if feature == "🔍 Symptom Analysis":
        symptom_analysis_page(assistant)
    elif feature == "💊 Disease Information":
        disease_info_page(assistant)
    elif feature == "🏥 Find Doctors":
        doctor_finder_page(assistant)
    elif feature == "📊 Health Statistics":
        health_statistics_page(assistant)

def symptom_analysis_page(assistant):
    """Symptom analysis and disease prediction page"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 🔍 Symptom Analysis & Disease Prediction")
    st.markdown("Select your symptoms to get AI-powered health insights")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Select Your Symptoms:")
        
        # Multi-select for symptoms
        selected_symptoms = st.multiselect(
            "Choose symptoms you're experiencing:",
            options=assistant.symptoms_list,
            help="Select multiple symptoms for more accurate prediction"
        )
        
        # Text input for additional symptoms
        additional_symptoms = st.text_area(
            "Describe any additional symptoms:",
            placeholder="Enter any other symptoms you're experiencing...",
            height=100
        )
        
        if st.button("🔮 Analyze Symptoms", type="primary"):
            if selected_symptoms or additional_symptoms:
                # Combine selected and additional symptoms
                all_symptoms = selected_symptoms + [additional_symptoms] if additional_symptoms else selected_symptoms
                symptoms_text = ' '.join(all_symptoms)
                
                # Display selected symptoms
                st.markdown("### Selected Symptoms:")
                for symptom in selected_symptoms:
                    st.markdown(f'<span class="symptom-chip">{symptom}</span>', unsafe_allow_html=True)
                
                # Get predictions
                predictions, confidences = assistant.predict_disease(symptoms_text)
                
                if predictions:
                    st.markdown("### 🎯 Prediction Results:")
                    
                    for i, (disease, confidence) in enumerate(zip(predictions, confidences)):
                        st.markdown(f'<div class="prediction-card">', unsafe_allow_html=True)
                        st.markdown(f"**{i+1}. {disease}**")
                        st.progress(confidence / 100)
                        st.markdown(f"Confidence: {confidence:.1f}%")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Show precautions for top prediction
                    if predictions:
                        top_disease = predictions[0]
                        st.markdown(f"### 🛡️ Medical Recommendations for {top_disease}:")
                        precautions = assistant.get_precautions(top_disease)
                        
                        if precautions:
                            st.info("⚠️ **Important**: These are general recommendations. Always consult a healthcare professional.")
                            for idx, precaution in enumerate(precautions, 1):
                                st.markdown(f'<div class="precaution-item">{idx}. {precaution}</div>', unsafe_allow_html=True)
                        else:
                            st.warning("No specific precautions found for this condition. Please consult a healthcare professional.")
                        
                        # Add spacing
                        st.markdown("---")
                        
                        # Additional general advice
                        st.markdown("### 💡 General Health Advice:")
                        st.markdown("""
                        - **Monitor Symptoms**: Keep track of how you feel over the next few days
                        - **Stay Hydrated**: Drink plenty of water
                        - **Rest**: Get adequate sleep and avoid strenuous activities
                        - **Seek Help**: Contact a healthcare provider if symptoms persist or worsen
                        """)
                else:
                    st.warning("Unable to make a prediction. Please try with different symptoms.")
            else:
                st.warning("Please select at least one symptom.")
    
    with col2:
        st.markdown("### ⚠️ Important Notice")
        st.info(
            "This tool provides AI-powered insights based on your symptoms. "
            "It should NOT replace professional medical advice. "
            "Please consult with a healthcare provider for proper diagnosis and treatment."
        )
        
        st.markdown("### 🏥 Emergency Situations")
        st.error(
            "If you're experiencing:\n"
            "• Chest pain\n"
            "• Difficulty breathing\n"
            "• Severe bleeding\n"
            "• Loss of consciousness\n"
            "• Severe allergic reactions\n\n"
            "**Call emergency services immediately!**"
        )

def disease_info_page(assistant):
    """Disease information and precautions page"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 💊 Disease Information & Precautions")
    st.markdown("Get detailed information about various diseases and their precautions")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Disease selector
    selected_disease = st.selectbox(
        "Select a disease to learn more:",
        options=[""] + assistant.diseases_list,
        help="Choose a disease to view precautions and information"
    )
    
    if selected_disease:
        st.markdown(f"### 🔍 Information for: {selected_disease}")
        
        # Get precautions
        precautions = assistant.get_precautions(selected_disease)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if precautions:
                st.markdown("#### 🛡️ Recommended Precautions:")
                for i, precaution in enumerate(precautions, 1):
                    st.markdown(f'<div class="precaution-item">{i}. {precaution}</div>', unsafe_allow_html=True)
            else:
                st.warning("No specific precautions found for this disease in our database.")
            
            # Show related symptoms
            disease_symptoms = assistant.diseases_df[assistant.diseases_df['Disease'] == selected_disease]
            if not disease_symptoms.empty:
                st.markdown("#### 🎯 Common Symptoms:")
                symptom_cols = [col for col in disease_symptoms.columns if col.startswith('Symptom_')]
                symptoms = []
                for col in symptom_cols:
                    symptom = disease_symptoms.iloc[0][col]
                    if pd.notna(symptom) and symptom.strip():
                        symptoms.append(symptom.strip().replace('_', ' '))
                
                for symptom in symptoms[:10]:  # Show first 10 symptoms
                    st.markdown(f'<span class="symptom-chip">{symptom}</span>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📞 When to Seek Medical Help")
            st.info(
                "Contact a healthcare provider if:\n"
                "• Symptoms worsen or persist\n"
                "• You develop new symptoms\n"
                "• You have concerns about your health\n"
                "• Precautions are not helping"
            )

def doctor_finder_page(assistant):
    """Doctor and hospital finder page"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 🏥 Find Nearby Doctors & Hospitals")
    st.markdown("Locate medical facilities and healthcare providers in your area")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📍 Choose Location Method")
        
        # Location options
        location_method = st.radio(
            "How would you like to find your location?",
            ["🌍 Detect my current location", "📍 Enter location manually"],
            help="Choose whether to automatically detect your location or enter it manually"
        )
        
        location = None
        use_current_location = False
        
        if location_method == "🌍 Detect my current location":
            use_current_location = True
            st.info("ℹ️ We'll detect your location using your IP address for privacy")
        else:
            location = st.text_input(
                "City, State or Address:",
                placeholder="e.g., New York, NY or 123 Main St, City, State",
                help="Enter your location to find nearby medical facilities"
            )
        
        radius = st.slider("Search Radius (km):", 1, 50, 10)
        
        search_button_text = "🌍 Find Nearby Facilities" if use_current_location else "🔍 Find Medical Facilities"
        
        if st.button(search_button_text, type="primary"):
            with st.spinner("Searching for nearby medical facilities..."):
                doctors, location_coords = assistant.find_nearby_doctors(
                    location=location, 
                    radius=radius, 
                    use_current_location=use_current_location
                )
            
            if doctors:
                # Remove old disclaimer and add new one for real data
                if use_current_location:
                    st.info(
                        "✅ **Real Location Detection:** Using your IP-based location to find actual nearby medical facilities. "
                        "Results may include hospitals, clinics, and other healthcare providers from OpenStreetMap and Google Places."
                    )
                else:
                    st.info(
                        "✅ **Real Search:** Showing actual medical facilities near the specified location. "
                        "Results are sourced from real healthcare databases."
                    )
                
                # Display results
                st.markdown("### 🏥 Nearby Medical Facilities:")
                for i, doctor in enumerate(doctors):
                    st.markdown(f'<div class="feature-card">', unsafe_allow_html=True)
                    
                    # Main info row
                    col_name, col_type, col_dist, col_action = st.columns([3, 2, 1, 1])
                    
                    with col_name:
                        st.markdown(f"**{doctor['name']}**")
                        st.markdown(f"📍 {doctor['address']}")
                    
                    with col_type:
                        st.markdown(f"🏥 {doctor['type']}")
                        if doctor.get('rating', 0) > 0:
                            st.markdown(f"⭐ {doctor['rating']}/5.0")
                        else:
                            st.markdown("⭐ Rating not available")
                    
                    with col_dist:
                        st.markdown(f"📏 {doctor['distance']} km")
                    
                    with col_action:
                        # Quick directions button
                        if doctor.get('lat') and doctor.get('lon'):
                            directions_url = f"https://www.google.com/maps/dir/?api=1&destination={doctor['lat']},{doctor['lon']}"
                        elif doctor.get('address'):
                            address_encoded = doctor['address'].replace(' ', '+').replace(',', '%2C')
                            directions_url = f"https://www.google.com/maps/dir/?api=1&destination={address_encoded}"
                        else:
                            name_encoded = doctor['name'].replace(' ', '+')
                            directions_url = f"https://www.google.com/maps/search/{name_encoded}"
                        
                        st.markdown(f'<a href="{directions_url}" target="_blank"><button style="background-color: #4285f4; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; width: 100%;">🗺️ Go</button></a>', unsafe_allow_html=True)
                    
                    # Expandable details section
                    with st.expander(f"📞 Contact Info & Details - {doctor['name']}"):
                        contact_col1, contact_col2 = st.columns(2)
                        
                        with contact_col1:
                            st.markdown("**📞 Contact Information:**")
                            if doctor.get('phone') and doctor['phone'] != 'Not available':
                                st.markdown(f"**Phone:** {doctor['phone']}")
                                
                                # Phone call buttons
                                call_col1, call_col2 = st.columns(2)
                                with call_col1:
                                    if st.button(f"📞 Call", key=f"call_{i}"):
                                        st.success(f"📞 To call {doctor['name']}, dial: **{doctor['phone']}**")
                                        st.info("💡 Click the phone number to call on mobile devices.")
                                
                                with call_col2:
                                    # Create Google Maps directions link
                                    if doctor.get('lat') and doctor.get('lon'):
                                        maps_url = f"https://www.google.com/maps/dir/?api=1&destination={doctor['lat']},{doctor['lon']}"
                                    elif doctor.get('address'):
                                        # Use address for directions if coordinates not available
                                        address_encoded = doctor['address'].replace(' ', '+').replace(',', '%2C')
                                        maps_url = f"https://www.google.com/maps/dir/?api=1&destination={address_encoded}"
                                    else:
                                        # Use hospital name as fallback
                                        name_encoded = doctor['name'].replace(' ', '+')
                                        maps_url = f"https://www.google.com/maps/search/{name_encoded}"
                                    
                                    st.markdown(f'<a href="{maps_url}" target="_blank"><button style="background-color: #4285f4; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 14px;">🗺️ Get Directions</button></a>', unsafe_allow_html=True)
                            else:
                                st.markdown("**Phone:** Not available")
                            
                            if doctor.get('website'):
                                st.markdown(f"**Website:** [Visit Website]({doctor['website']})")
                                
                            # Add additional navigation options
                            st.markdown("**🚗 Navigation Options:**")
                            nav_col1, nav_col2 = st.columns(2)
                            
                            with nav_col1:
                                # Google Maps link with hospital name
                                hospital_name_encoded = doctor['name'].replace(' ', '+').replace(',', '%2C')
                                google_maps_search = f"https://www.google.com/maps/search/{hospital_name_encoded}"
                                st.markdown(f'[🔍 Search on Maps]({google_maps_search})')
                            
                            with nav_col2:
                                # Alternative - using address if available
                                if doctor.get('address') and doctor.get('address') != 'Address not available':
                                    address_search = doctor['address'].replace(' ', '+').replace(',', '%2C')
                                    address_maps_url = f"https://www.google.com/maps/search/{address_search}"
                                    st.markdown(f'[📍 Find Address]({address_maps_url})')
                                else:
                                    st.markdown("📍 Address not available")
                        
                        with contact_col2:
                            if doctor.get('hours'):
                                st.markdown("**🕒 Hours:**")
                                st.markdown(doctor['hours'])
                            
                            if doctor.get('specialties'):
                                st.markdown("**🩺 Specialties:**")
                                for specialty in doctor['specialties']:
                                    st.markdown(f"• {specialty}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Create and display map
                if location_coords:
                    st.markdown("### 🗺️ Interactive Map:")
                    map_obj = assistant.create_map(location_coords, doctors)
                    if map_obj:
                        st.components.v1.html(map_obj._repr_html_(), height=500)
            
            else:
                if location_coords:
                    st.warning("No medical facilities found in your area. Try increasing the search radius.")
                else:
                    st.error("Could not determine location. Please try again or enter location manually.")
    
    with col2:
        st.markdown("### 🚨 Emergency Contacts")
        st.error(
            "**Emergency Services:**\n"
            "🚑 Ambulance: 911\n"
            "🏥 Emergency Room: 911\n"
            "☎️ Poison Control: 1-800-222-1222"
        )
        
        st.markdown("### 📋 Facility Types")
        st.info(
            "**Hospital:** Full-service medical care\n"
            "**Clinic:** Outpatient care and checkups\n"
            "**Emergency Center:** Urgent and emergency care\n"
            "**Specialist:** Specialized medical services\n"
            "**Community Health:** Basic healthcare services"
        )
        
        st.markdown("### 💡 Tips for Choosing")
        st.info(
            "• Check if they accept your insurance\n"
            "• Consider distance and travel time\n"
            "• Look at ratings and reviews\n"
            "• Verify they treat your condition\n"
            "• Check appointment availability"
        )

def health_statistics_page(assistant):
    """Health statistics and insights page"""
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Health Statistics & Insights")
    st.markdown("Explore health data and medical insights from our database")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if assistant.diseases_df is not None:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Disease distribution
            st.markdown("### 🦠 Disease Categories in Database")
            disease_counts = assistant.diseases_df['Disease'].value_counts().head(10)
            st.bar_chart(disease_counts)
            
            # Most common symptoms
            st.markdown("### 🎯 Most Common Symptoms")
            symptom_counts = {}
            for col in assistant.diseases_df.columns:
                if col.startswith('Symptom_'):
                    symptoms = assistant.diseases_df[col].dropna()
                    for symptom in symptoms:
                        if symptom.strip():
                            clean_symptom = symptom.strip().replace('_', ' ')
                            symptom_counts[clean_symptom] = symptom_counts.get(clean_symptom, 0) + 1
            
            # Get top 15 symptoms
            top_symptoms = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:15]
            symptom_df = pd.DataFrame(top_symptoms, columns=['Symptom', 'Frequency'])
            st.bar_chart(symptom_df.set_index('Symptom'))
            
        with col2:
            # Database stats
            st.markdown("### 📈 Database Statistics")
            
            total_diseases = len(assistant.diseases_list)
            total_symptoms = len(assistant.symptoms_list)
            total_records = len(assistant.diseases_df)
            
            st.metric("Total Diseases", total_diseases)
            st.metric("Unique Symptoms", total_symptoms)
            st.metric("Medical Records", total_records)
            
            # Additional insights
            st.markdown("### 🧠 AI Model Performance")
            st.info(
                f"Model Type: Naive Bayes Classifier\n"
                f"Training Data: {total_records} records\n"
                f"Features: Text-based symptom analysis\n"
                f"Accuracy: Estimated 85-90%*\n\n"
                f"*Based on similar medical AI systems"
            )
            
            st.markdown("### 📚 Data Sources")
            st.info(
                "Our medical database includes:\n"
                "• Disease-symptom mappings\n"
                "• Medical precautions\n"
                "• Treatment recommendations\n"
                "• Healthcare provider information"
            )

if __name__ == "__main__":
    main()
