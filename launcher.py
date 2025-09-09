#!/usr/bin/env python3
"""
Launcher script for the Intelligent Healthcare Assistant
This script sets up the environment and launches the Streamlit application
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'scikit-learn',
        'requests',
        'folium',
        'geopy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            if package == 'scikit-learn':
                try:
                    __import__('sklearn')
                except ImportError:
                    missing_packages.append(package)
            else:
                missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   • {package}")
        print("\n📦 Installing missing packages...")
        
        # Install missing packages
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ Successfully installed {package}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def check_data_files():
    """Check if required data files exist"""
    required_files = [
        'DiseaseAndSymptoms.csv',
        'Disease precaution.csv'
    ]
    
    missing_files = []
    current_dir = Path.cwd()
    
    for file in required_files:
        if not (current_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required data files:")
        for file in missing_files:
            print(f"   • {file}")
        print("\n📂 Please ensure these files are in the current directory:")
        print(f"   {current_dir}")
        return False
    
    return True

def launch_app():
    """Launch the Streamlit application"""
    print("🚀 Launching Healthcare Assistant...")
    print("📱 The application will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("\n⚠️  To stop the application, press Ctrl+C in this terminal")
    
    try:
        # Launch Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Healthcare Assistant stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🏥 INTELLIGENT HEALTHCARE ASSISTANT LAUNCHER")
    print("=" * 60)
    print()
    
    # Check Python version
    print("🐍 Checking Python version...")
    if not check_python_version():
        return
    print("✅ Python version is compatible")
    
    # Check required packages
    print("\n📦 Checking required packages...")
    if not check_requirements():
        print("❌ Failed to install required packages")
        return
    print("✅ All required packages are available")
    
    # Check data files
    print("\n📊 Checking data files...")
    if not check_data_files():
        return
    print("✅ All data files found")
    
    print("\n🎉 All checks passed! Ready to launch...")
    print()
    
    # Launch application
    launch_app()

if __name__ == "__main__":
    main()
