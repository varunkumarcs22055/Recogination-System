# 🔐 Face Recognition & Liveness Detection System

A complete **local, privacy-safe face recognition system** with real-time camera feedback and anti-spoofing liveness detection. No cloud services, no external APIs, 100% offline!

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![Gradio](https://img.shields.io/badge/Gradio-4.7-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Key Features

- 👁️ **Real-time Camera Feedback** - Live quality checks and face detection
- 🎯 **Smart Face Recognition** - Multi-algorithm feature fusion for high accuracy
- 🔒 **100% Privacy** - All processing happens locally, no cloud services
- 🚫 **Anti-Spoofing** - Liveness detection using texture analysis
- 🌐 **Web Interface** - Clean, modern Gradio UI
- 📊 **Admin Panel** - Manage registered users easily
- 🎨 **Quality Checks** - Blur detection, brightness validation, face size verification

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/varunkumarcs22055/Recogination-System.git
cd Recogination-System/face_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
# Windows (recommended)
.\run_app.bat

# Or manually
python app_perfect.py
```

The app will open at **http://127.0.0.1:7860**

## 📖 Documentation

- 📋 [Detailed Documentation](face_app/README.md) - Full feature list and usage guide
- 🛠️ [Installation Guide](face_app/INSTALL.md) - Detailed setup instructions
- 📝 [Project Overview](face_app/PROJECT.md) - Technical details

## 🎯 How It Works

1. **Verify Identity** - Real-time camera shows quality feedback
2. **Capture Face** - Click when status shows "✅ Face detected! Good quality"
3. **Register New User** - If not recognized, register with your name
4. **Admin Panel** - View and manage all registered users

## 🔧 Technical Stack

- **face_recognition** - Face detection and encoding
- **OpenCV** - Image processing and computer vision
- **MediaPipe** - Facial landmark detection
- **Gradio** - Modern web interface
- **NumPy** - Numerical computing

## 📋 Requirements

- Python 3.9+
- Webcam/Camera
- Windows/Linux/macOS

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Varun Kumar**
- GitHub: [@varunkumarcs22055](https://github.com/varunkumarcs22055)

---

⭐ Star this repo if you find it useful!