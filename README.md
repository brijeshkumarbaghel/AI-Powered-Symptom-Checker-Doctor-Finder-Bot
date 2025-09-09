# 🏥 Intelligent Healthcare Assistant

An AI-Powered Symptom Checker & Doctor Finder Bot that helps users analyze symptoms, predict possible diseases, and locate nearby medical facilities.

## 🌟 Features

### 🔍 Symptom Analysis
- **AI-Powered Disease Prediction**: Uses machine learning to analyze symptoms and predict possible diseases
- **Multi-Symptom Input**: Select from a comprehensive list of symptoms or describe additional symptoms
- **Confidence Scoring**: Shows prediction confidence levels for better decision-making
- **Real-time Analysis**: Instant results with interactive interface

### 💊 Disease Information
- **Comprehensive Database**: Information on various diseases and their symptoms
- **Medical Precautions**: Detailed precautions and recommendations for each disease
- **Symptom Mapping**: View common symptoms associated with specific diseases
- **Treatment Guidelines**: Basic treatment and care recommendations

### 🏥 Doctor & Hospital Finder
- **Location-Based Search**: Find nearby medical facilities using your location
- **Interactive Maps**: Visual representation of medical facilities in your area
- **Facility Information**: Details about hospitals, clinics, specialists, and emergency centers
- **Distance & Ratings**: Distance calculations and facility ratings

### 📊 Health Statistics
- **Medical Data Insights**: Visualize disease and symptom patterns from the database
- **AI Model Performance**: Information about the machine learning model accuracy
- **Database Statistics**: Overview of available medical data

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**
   ```bash
   cd "AI-Powered Symptom Checker & Doctor Finder Bot"
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify data files**
   Ensure these files are in the project directory:
   - `DiseaseAndSymptoms.csv`
   - `Disease precaution.csv`

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   The app will automatically open in your default browser at `http://localhost:8501`

## 💻 Usage Guide

### Symptom Analysis
1. Navigate to "🔍 Symptom Analysis"
2. Select symptoms from the dropdown menu
3. Add additional symptoms in the text area (optional)
4. Click "🔮 Analyze Symptoms"
5. Review the AI predictions and recommended precautions

### Disease Information
1. Go to "💊 Disease Information"
2. Select a disease from the dropdown
3. View precautions and common symptoms
4. Get guidance on when to seek medical help

### Doctor Finder
1. Access "🏥 Find Doctors"
2. Enter your location (city, state, or address)
3. Adjust the search radius
4. Click "🔍 Find Medical Facilities"
5. View results and interactive map

### Health Statistics
1. Visit "📊 Health Statistics"
2. Explore disease distribution charts
3. View most common symptoms
4. Check database and AI model statistics

## 🗂️ Project Structure

```
AI-Powered Symptom Checker & Doctor Finder Bot/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── DiseaseAndSymptoms.csv     # Disease-symptom mapping dataset
├── Disease precaution.csv     # Disease precautions dataset
├── README.md                  # This file
└── .gitignore                 # Git ignore file
```

## 🔧 Technical Details

### Machine Learning Model
- **Algorithm**: Multinomial Naive Bayes Classifier
- **Feature Extraction**: TF-IDF Vectorization
- **Training Data**: Disease-symptom mappings from CSV dataset
- **Prediction**: Multi-class classification with confidence scoring

### Data Processing
- **Symptom Normalization**: Converts underscores to spaces, removes duplicates
- **Disease Mapping**: Maps symptoms to diseases using the provided dataset
- **Precaution Matching**: Links diseases to their corresponding precautions

### Location Services
- **Geocoding**: Uses Nominatim (OpenStreetMap) for location processing
- **Map Visualization**: Interactive maps with Folium
- **Distance Calculation**: Calculates distances to nearby facilities

## ⚠️ Important Disclaimers

### Medical Advice
- This application is for **informational purposes only**
- It should **NOT replace professional medical advice**
- Always consult with qualified healthcare providers for proper diagnosis
- In case of emergency, contact emergency services immediately

### AI Limitations
- Predictions are based on pattern recognition in training data
- Medical conditions can be complex and require professional evaluation
- The AI model may not account for all possible symptoms or conditions

### Emergency Situations
**Seek immediate medical attention for:**
- Chest pain or difficulty breathing
- Severe bleeding or trauma
- Loss of consciousness
- Severe allergic reactions
- Signs of stroke or heart attack

## 🔮 Future Enhancements

### Planned Features
- **Integration with Real APIs**: Google Places API for actual doctor/hospital data
- **Appointment Booking**: Direct integration with healthcare provider systems
- **Symptom Tracking**: Personal health tracking and history
- **Multi-language Support**: Support for multiple languages
- **Mobile App**: Native mobile application
- **Telemedicine Integration**: Video consultation capabilities

### Technical Improvements
- **Advanced ML Models**: Deep learning and neural network implementations
- **Real-time Data Updates**: Live medical database updates
- **User Authentication**: Secure user accounts and data storage
- **Advanced Analytics**: Personalized health insights and recommendations

## 🤝 Contributing

We welcome contributions to improve the Healthcare Assistant! Here's how you can help:

1. **Report Issues**: Submit bug reports or feature requests
2. **Improve Data**: Help expand the medical database
3. **Code Contributions**: Submit pull requests with improvements
4. **Documentation**: Help improve documentation and user guides
5. **Testing**: Test the application and provide feedback

## 📄 License

This project is designed for educational and demonstration purposes. Please ensure compliance with healthcare regulations and data privacy laws in your jurisdiction.

## 🙋‍♀️ Support

For questions, issues, or suggestions:
- Check the existing documentation
- Review common issues and solutions
- Submit detailed bug reports with steps to reproduce

## 🌐 Acknowledgments

- **Medical Data**: Based on publicly available medical datasets
- **Streamlit**: For the excellent web framework
- **Scikit-learn**: For machine learning capabilities
- **OpenStreetMap**: For location services via Nominatim

---

**Remember**: This tool is designed to assist and inform, but should never replace professional medical advice. Always consult with healthcare providers for proper medical care and treatment.
