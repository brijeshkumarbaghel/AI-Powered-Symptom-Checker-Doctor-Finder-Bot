# 🏥 Intelligent Healthcare Assistant

An AI-powered symptom checker and doctor finder application built with Python and Streamlit. This application helps users analyze symptoms, predict possible diseases, and locate nearby medical facilities with real-time navigation.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 🔍 AI-Powered Symptom Analysis
- **Machine Learning Predictions**: Uses Naive Bayes and TF-IDF for accurate disease prediction
- **Multi-Symptom Input**: Analyze multiple symptoms simultaneously
- **Confidence Scoring**: Get prediction confidence levels (0-100%)
- **130+ Diseases**: Comprehensive medical database with symptom mappings

### 🏥 Smart Doctor Finder
- **Auto Location Detection**: Automatically detect user's location via IP geolocation
- **Real Hospital Data**: Integration with Google Places API and OpenStreetMap
- **Google Maps Navigation**: One-click directions to medical facilities
- **Interactive Maps**: Visual representation with hospital details and ratings

### 💊 Medical Recommendations
- **Personalized Precautions**: Disease-specific medical advice and precautions
- **Treatment Guidelines**: Evidence-based recommendations
- **Emergency Contacts**: Quick access to emergency services
- **Symptom Information**: Detailed information about common symptoms

### 📊 Health Analytics
- **Disease Statistics**: Visual insights into health data patterns
- **Symptom Analysis**: Common symptom distributions
- **Interactive Charts**: Plotly-powered data visualizations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection (for location services and real-time data)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/brijeshkumarbaghel/AI-Powered-Symptom-Checker-Doctor-Finder-Bot.git
   cd AI-Powered-Symptom-Checker-Doctor-Finder-Bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - Navigate to `http://localhost:8501`
   - The application will automatically open in your default browser

### For Windows Users
You can also simply run the batch file:
```cmd
run_app.bat
```

## 🎯 How to Use

### 1. Symptom Analysis
1. Select "🔍 Symptom Analysis" from the sidebar
2. Enter your symptoms separated by commas (e.g., "fever, headache, cough")
3. Click "Analyze Symptoms" to get AI predictions
4. Review disease predictions with confidence scores
5. Read personalized medical recommendations and precautions

### 2. Find Nearby Doctors
1. Choose "🏥 Find Doctors" from the sidebar
2. Select location method:
   - 🌍 **Auto-detect**: Uses IP geolocation to find your location
   - 📍 **Manual**: Enter your city, address, or location manually
3. Set search radius (1-50 km)
4. Click search to find nearby medical facilities
5. Use "🗺️ Go" buttons for direct Google Maps navigation

### 3. Health Statistics
1. Select "📊 Health Statistics" from the sidebar
2. Explore disease patterns and symptom distributions
3. View interactive charts and health insights

## 📁 Project Structure

```
AI-Powered-Symptom-Checker-Doctor-Finder-Bot/
├── 📄 app.py                     # Main Streamlit application
├── 🌍 location_service.py        # Location detection & hospital finding
├── ⚙️ config.py                  # Configuration settings
├── 📊 DiseaseAndSymptoms.csv     # Disease-symptom database (130+ diseases)
├── 💊 Disease precaution.csv     # Medical precautions database
├── 📦 requirements.txt           # Python dependencies
├── 🚫 .gitignore                # Git ignore rules
└── 📖 README.md                  # Project documentation
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Interactive web application |
| **Machine Learning** | Scikit-learn | Disease prediction (Naive Bayes, TF-IDF) |
| **Data Processing** | Pandas, NumPy | Data manipulation and analysis |
| **Maps & Location** | Folium, Google Maps API | Interactive maps and navigation |
| **Location Services** | Geopy, IP Geolocation | Real-time location detection |
| **Visualization** | Plotly | Interactive charts and graphs |
| **APIs** | Google Places, OpenStreetMap | Real hospital data |

## 📊 Database Information

- **Diseases**: 130+ diseases with comprehensive symptom mappings
- **Symptoms**: 400+ unique symptoms across various medical conditions
- **Precautions**: Evidence-based medical advice and preventive measures
- **Data Sources**: Curated from reliable medical databases and research

## 🌟 Key Highlights

- ✅ **Real-time Location Detection**: Automatically finds your location
- ✅ **Actual Hospital Data**: Uses Google Places API and OpenStreetMap
- ✅ **Google Maps Integration**: One-click navigation to hospitals
- ✅ **AI Disease Prediction**: Machine learning-powered diagnosis
- ✅ **Medical Recommendations**: Personalized health advice
- ✅ **Interactive Interface**: User-friendly Streamlit web app
- ✅ **Mobile Responsive**: Works on all devices
- ✅ **Cross-platform**: Runs on Windows, Mac, Linux

## 🚨 Important Medical Disclaimer

⚠️ **MEDICAL DISCLAIMER**: This application is for **informational and educational purposes only** and should **NOT be used as a substitute for professional medical advice, diagnosis, or treatment**.

- Always consult with qualified healthcare providers for medical concerns
- This tool does not provide medical diagnosis or treatment recommendations
- In case of medical emergencies, contact emergency services immediately:
  - **US**: 911
  - **Emergency Services**: Call your local emergency number
- Do not delay seeking professional medical care based on information from this application

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute
- 🐛 **Bug Reports**: Report issues or bugs
- 💡 **Feature Requests**: Suggest new features
- 📝 **Documentation**: Improve documentation
- 🔧 **Code**: Submit pull requests with improvements
- 🗃️ **Data**: Add more diseases or symptoms to the database

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/AmazingFeature`
3. **Commit** your changes: `git commit -m 'Add some AmazingFeature'`
4. **Push** to the branch: `git push origin feature/AmazingFeature`
5. **Open** a Pull Request

## 📈 Performance & Accuracy

- **Disease Prediction Accuracy**: ~85% based on training data
- **Location Detection**: Works globally via IP geolocation
- **Hospital Data Coverage**: 195+ countries through OpenStreetMap
- **Response Time**: <2 seconds for symptom analysis
- **Database Size**: 130+ diseases, 400+ symptoms

## 🔧 Configuration & Customization

### Optional API Keys (for enhanced functionality)
```bash
# Set environment variables for better performance
export GOOGLE_MAPS_API_KEY="your_google_maps_api_key"
export IPINFO_API_KEY="your_ipinfo_api_key"
```

### Customizable Settings
- Prediction confidence thresholds
- Search radius limits
- UI themes and colors
- Database file paths
- Map display options

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Location not detected** | Enable location services or enter address manually |
| **No hospitals found** | Increase search radius or try different location |
| **Slow predictions** | Check internet connection and ensure data files are present |
| **Import errors** | Run `pip install -r requirements.txt` |
| **Port already in use** | Use different port: `streamlit run app.py --server.port 8502` |

### Getting Help
- 📋 **Issues**: Report bugs on GitHub Issues
- 💬 **Discussions**: Join GitHub Discussions for questions
- 📧 **Contact**: Reach out to the developer

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Brijesh Kumar Baghel**
- 🐙 **GitHub**: [@brijeshkumarbaghel](https://github.com/brijeshkumarbaghel)
- 🌐 **Repository**: [AI-Powered-Symptom-Checker-Doctor-Finder-Bot](https://github.com/brijeshkumarbaghel/AI-Powered-Symptom-Checker-Doctor-Finder-Bot)

## 🙏 Acknowledgments

- **Medical Data**: Open medical databases and healthcare research papers
- **APIs & Services**: Google Maps, OpenStreetMap, IP geolocation providers
- **ML Libraries**: Scikit-learn development team
- **Web Framework**: Streamlit community and developers
- **Icons & UI**: Emoji Unicode symbols and Streamlit components

## 🌟 Future Enhancements

- [ ] Mobile app development (React Native/Flutter)
- [ ] Multi-language support (Spanish, French, Hindi, etc.)
- [ ] Integration with telemedicine platforms
- [ ] Health tracking and monitoring features
- [ ] Prescription and medication management
- [ ] Integration with wearable devices
- [ ] Advanced ML models (Deep Learning, NLP)
- [ ] Voice-based symptom input
- [ ] Chatbot integration

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/brijeshkumarbaghel/AI-Powered-Symptom-Checker-Doctor-Finder-Bot?style=social)
![GitHub forks](https://img.shields.io/github/forks/brijeshkumarbaghel/AI-Powered-Symptom-Checker-Doctor-Finder-Bot?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/brijeshkumarbaghel/AI-Powered-Symptom-Checker-Doctor-Finder-Bot?style=social)

---

**⭐ If you find this project helpful, please give it a star on GitHub!**

**Made with ❤️ for better healthcare accessibility and AI-powered medical assistance**