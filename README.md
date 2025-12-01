# 🔐 Face Recognition System# 🔐 Face Recognition & Liveness Detection System



A powerful, offline face recognition system with liveness detection built using OpenCV and Gradio. Fast, accurate, and runs 100% locally on your machine.A complete **local, privacy-safe face recognition system** with anti-spoofing liveness detection. No cloud services, no external APIs, 100% offline!



![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

![OpenCV](https://img.shields.io/badge/OpenCV-4.12+-green.svg)![License](https://img.shields.io/badge/License-MIT-green.svg)

![Gradio](https://img.shields.io/badge/Gradio-4.19-orange.svg)![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)



## ✨ Features## ✨ Features



- ✅ **Fast Face Recognition** - Advanced 6-algorithm feature fusion for high accuracy- ✅ **Multi-sample Face Recognition** - Store multiple face images per user for improved accuracy

- ✅ **Single Image Registration** - Only one photo needed per person- 👁️ **Liveness Detection** - Anti-spoofing protection using texture-based analysis

- ✅ **Web Interface** - Clean, modern UI with Gradio- 🔒 **100% Local** - No cloud services, no external APIs, complete privacy

- ✅ **Admin Panel** - Manage registered users easily- 📁 **JSON Storage** - Simple JSON-based database with local image storage

- ✅ **100% Offline** - No cloud services, complete privacy- 🎨 **Dual Interface** - Both Gradio web UI and command-line interface

- ✅ **Real-time Verification** - Instant face matching- 🚫 **Multi-face Rejection** - Automatically rejects images with multiple faces

- ✅ **Visual Guide** - Oval face guide for perfect alignment- 📊 **Confidence Scoring** - Shows match confidence percentage

- ✅ **Quality Enhancement** - CLAHE image processing for better accuracy- 🌐 **Open Source** - Built entirely with free, open-source libraries



## 🎯 Accuracy## 🧩 Technical Stack



- **Recognition Threshold**: 60% (adjustable)- **face_recognition** - Face detection and encoding

- **Feature Algorithms**: - **OpenCV** - Image processing and computer vision

  - LBP (Local Binary Patterns) - 35%- **MediaPipe** - Advanced facial landmark detection (optional for blink detection)

  - HOG (Histogram of Oriented Gradients) - 30%- **Gradio** - Modern web interface

  - Color Histograms - 15%- **dlib** - Machine learning toolkit (backend for face_recognition)

  - Gray Histograms - 10%

  - Edge Patterns - 10%## 📁 Project Structure



## 📋 Requirements```

face_app/

- Windows 10/11├── app.py              # Main application (GUI + CLI)

- Python 3.9 or higher├── utils.py            # Helper functions for face processing

- Webcam├── requirements.txt    # Python dependencies

- 4GB RAM minimum├── faces.json          # User database (auto-created)

- Internet connection (for initial setup only)├── faces/              # Stored face images

│   ├── Varun_1_*.jpg

## 🚀 Quick Start│   ├── Varun_2_*.jpg

│   └── ...

### 1. Install Dependencies└── README.md           # This file

```

```powershell

# Create virtual environment## 🚀 Installation

python -m venv venv

### Prerequisites

# Activate virtual environment

.\venv\Scripts\Activate.ps1**Windows Users:**

1. Install [CMake](https://cmake.org/download/)

# Install requirements2. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)

pip install -r requirements.txt   - Select "Desktop development with C++"

```

**Linux Users:**

### 2. Run the Application```bash

sudo apt-get update

```powershellsudo apt-get install build-essential cmake

# Start the appsudo apt-get install libopenblas-dev liblapack-dev

python app_perfect.pysudo apt-get install libx11-dev libgtk-3-dev

``````



Or double-click `run_app.bat`**macOS Users:**

```bash

### 3. Access the Web Interfacebrew install cmake

```

Open your browser and go to:

```### Step 1: Clone or Download

http://127.0.0.1:7860

``````bash

cd "c:\Users\vt690\Desktop\Recogination System\face_app"

## 📖 Usage Guide```



### Register a New User### Step 2: Create Virtual Environment (Recommended)



1. Open the app in your browser```bash

2. Go to **"👤 Verify Identity"** tabpython -m venv venv

3. Allow camera access

4. Position your face in the green oval guide# Windows

5. Click the webcam snapshot buttonvenv\Scripts\activate

6. Click **"Capture & Verify"**

7. When prompted, click **"Register Me"**# Linux/macOS

8. Enter your full namesource venv/bin/activate

9. Click **"✅ Register Me"**```



### Verify Identity### Step 3: Install Dependencies



1. Go to **"👤 Verify Identity"** tab```bash

2. Position your face in the oval guidepip install --upgrade pip

3. Click the webcam snapshot buttonpip install -r requirements.txt

4. Click **"🎯 Capture & Verify"**```

5. System will recognize you instantly!

**Note:** If `dlib` installation fails on Windows, try:

### Manage Users (Admin Panel)```bash

pip install dlib-binary

1. Go to **"⚙️ Admin Panel"** tab```

2. View all registered users

3. Delete users if neededOr download a pre-compiled wheel from [here](https://github.com/z-mahmud22/Dlib_Windows_Python3.x).

4. Refresh the list anytime

## 🎯 Usage

## 🌐 Public Access (Optional)

### 🌐 Web Interface (Gradio)

To share your app publicly using ngrok:

Launch the web interface:

```powershell

# Simple way (no auth needed)```bash

ngrok http 7860python app.py

```

# With authentication

ngrok http 7860 --basic-auth="username:password"The app will open at `http://127.0.0.1:7860` in your default browser.

```

**Features:**

Copy the public URL and share it!- 🔍 **Verify Face** - Check if a face matches any registered user

- 📝 **Register New User** - Add a new user to the database

## 📁 Project Structure- 👥 **Registered Users** - View all registered users



```### 💻 Command-Line Interface

face_app/

├── app_perfect.py      # Main applicationLaunch in CLI mode:

├── faces.json          # User database (auto-created)

├── faces/              # Stored face images (auto-created)```bash

├── requirements.txt    # Python dependenciespython app.py --cli

├── run_app.bat         # Quick launcher```

├── README.md           # This file

└── venv/               # Virtual environment**Menu Options:**

```1. Verify Face

2. Register New User

## 🔧 Configuration3. List Registered Users

4. Exit

Edit these values in `app_perfect.py` if needed:

### 📸 Example Workflow

```python

BASE_THRESHOLD = 0.60    # Recognition threshold (0.0 - 1.0)#### Web Interface:

MIN_FACE_SIZE = 150      # Minimum face size in pixels1. Go to **"Register New User"** tab

SERVER_PORT = 7860       # Web server port2. Enter your name (e.g., "Varun")

```3. Upload a photo or use webcam

4. Click **"Register"**

## 🛠️ Troubleshooting5. Go to **"Verify Face"** tab

6. Upload/capture another photo

### Camera Not Working7. See recognition result!

- Allow camera permissions in browser

- Check if another app is using the camera#### CLI:

- Try refreshing the page```bash

python app.py --cli

### Low Accuracy

- Ensure good lighting>> Select option: 2

- Face the camera directly>> Enter name: Varun

- Remove glasses if possible>> Enter path to image: C:\Users\vt690\Pictures\my_face.jpg

- Re-register with a clearer photo>> ✅ Registered successfully!



### Port Already in Use>> Select option: 1

- Close other apps using port 7860>> Enter path to image: C:\Users\vt690\Pictures\my_face2.jpg

- Or change `SERVER_PORT` in the code>> ✅ Access Granted. Welcome back, Varun! (Confidence: 87.3%)

```

### Database Issues

- Delete `faces.json` to reset## 🔧 How It Works

- Delete `faces/` folder to clear all images

- Restart the app### Face Recognition Flow



## 🎨 Tips for Best Results```

┌─────────────────┐

- ✅ **Good Lighting**: Natural, even lighting works best│  Upload Image   │

- ✅ **Clear Background**: Avoid busy backgrounds└────────┬────────┘

- ✅ **Face Camera**: Look directly at the camera         │

- ✅ **No Glasses**: Better recognition without glasses         ▼

- ✅ **Neutral Expression**: Works better than smiling┌─────────────────┐

- ✅ **Stable Camera**: Hold still when capturing│ Detect Faces    │ ──► Multiple faces? ──► ❌ Reject

└────────┬────────┘

## 📊 Technical Details         │ Single face ✓

         ▼

### Face Detection┌─────────────────┐

- OpenCV Haar Cascade Classifier│ Liveness Check  │ ──► Failed? ──► ❌ Reject (Spoofing detected)

- Multi-scale detection└────────┬────────┘

- Fast and accurate         │ Passed ✓

         ▼

### Feature Extraction┌─────────────────┐

- Multi-radius LBP for texture analysis│ Face Encoding   │

- Weighted HOG for gradient patterns└────────┬────────┘

- HSV color histograms         │

- Spatial gray histograms         ▼

- Edge density patterns┌─────────────────┐

│ Match w/ DB     │ ──► No match? ──► Offer registration

### Image Enhancement└────────┬────────┘

- CLAHE (Contrast Limited Adaptive Histogram Equalization)         │ Match ✓

- Automatic brightness adjustment         ▼

- Noise reduction┌─────────────────┐

│ ✅ Access       │

### Database│   Granted!      │

- JSON format for easy editing└─────────────────┘

- Pre-computed features for speed```

- Automatic backup on save

### Liveness Detection

## 🔐 Privacy & Security

The system uses **texture-based analysis** to detect spoofing attempts:

- ✅ **100% Offline**: No data sent to cloud

- ✅ **Local Storage**: All data stays on your machine1. **Texture Complexity** - Real skin has micro-details; photos are too smooth

- ✅ **No Tracking**: No analytics or telemetry2. **Color Variation** - Natural skin has color variation; screens/prints are uniform

- ✅ **Open Source**: Review the code yourself3. **Edge Density** - Checks for unnatural edge patterns



## 🚀 Performance**Thresholds:**

- Laplacian variance < 50 → Likely a photo

- **Registration**: < 1 second- Saturation std < 10 → Likely a screen/print

- **Verification**: < 0.5 seconds- Edge density > 0.3 → Might be printed

- **Database Size**: ~2KB per user

- **Image Size**: ~100KB per user### Face Matching

- **RAM Usage**: ~200MB

- **Encoding**: Each face is converted to a 128-dimensional vector

## 📝 License- **Comparison**: Uses Euclidean distance between vectors

- **Threshold**: Distance ≤ 0.6 for a match

This project is open source. Feel free to use and modify.- **Multi-sample**: Compares against ALL stored encodings for a user and uses the best match



## 🤝 Contributing## 📊 Database Format



Suggestions and improvements are welcome!`faces.json`:

```json

## 📧 Support{

  "users": [

If you encounter any issues:    {

1. Check the Troubleshooting section      "name": "Varun",

2. Review the code comments      "encodings": [

3. Check camera permissions        [0.112, -0.331, 0.499, ...],

4. Restart the application        [0.221, -0.129, 0.338, ...]

      ],

## 🎯 Future Enhancements      "images": [

        "faces/Varun_1_20251026_143022.jpg",

- [ ] Multiple camera support        "faces/Varun_2_20251026_143145.jpg"

- [ ] Batch registration      ]

- [ ] Export/Import users    }

- [ ] Face mask detection  ]

- [ ] Age/Gender detection}

- [ ] Attendance logging```

- [ ] Email notifications

## ⚙️ Configuration

## 📚 Dependencies

Edit these values in `app.py` or `utils.py`:

- **OpenCV**: Face detection and image processing

- **NumPy**: Numerical computations```python

- **Gradio**: Web interface# Face matching threshold (lower = more strict)

- **Pillow**: Image handlingthreshold = 0.6  # Default: 0.6



## ⭐ Acknowledgments# Liveness detection thresholds

LAPLACIAN_THRESHOLD = 50

Built with:SATURATION_STD_THRESHOLD = 10

- OpenCV for computer visionEDGE_DENSITY_THRESHOLD = 0.3

- Gradio for the amazing UI framework```

- NumPy for fast computations

## 🛡️ Security & Privacy

---

- ✅ **100% Local** - All processing happens on your machine

**Made with ❤️ for secure, offline face recognition**- ✅ **No Internet Required** - Works completely offline

- ✅ **No Cloud Storage** - All data stays on your device

*Last Updated: October 27, 2025*- ✅ **Open Source** - Fully transparent code

- ✅ **Liveness Protection** - Guards against photo/video spoofing

## 🐛 Troubleshooting

### dlib Installation Failed

**Windows:**
```bash
pip install cmake
pip install dlib-binary
```

Or download from: https://github.com/z-mahmud22/Dlib_Windows_Python3.x

**Linux:**
```bash
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
pip install dlib
```

### "No face detected"

- Ensure good lighting
- Face should be clearly visible and centered
- Try a higher resolution image
- Remove obstructions (sunglasses, masks, etc.)

### "Liveness check failed"

- Use a real face, not a photo or screen
- Ensure proper lighting (not too bright/dark)
- Try adjusting liveness thresholds in `utils.py`

### Low Recognition Accuracy

- Register multiple photos from different angles
- Ensure consistent lighting
- Lower the threshold (e.g., 0.5 instead of 0.6)
- Use higher quality images

## 📈 Performance Tips

1. **Multiple Samples**: Register 2-3 photos per user for better accuracy
2. **Good Lighting**: Well-lit photos work best
3. **Consistent Angles**: Register photos from similar angles you'll verify with
4. **High Quality**: Use high-resolution images (at least 640x480)
5. **Proper Distance**: Face should be clearly visible, not too close or far

## 🔮 Future Enhancements

- [ ] Real-time blink detection using video frames
- [ ] Head movement tracking for enhanced liveness
- [ ] Support for multiple face databases
- [ ] Export/import database functionality
- [ ] Face embedding visualization (t-SNE/PCA)
- [ ] Training history and analytics
- [ ] Batch registration from folder
- [ ] Face aging tolerance adjustments

## 📜 License

MIT License - Feel free to use, modify, and distribute!

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📞 Support

Having issues? Check:
1. This README's troubleshooting section
2. Requirements are properly installed
3. Python version is 3.8 or higher
4. Face images meet quality guidelines

## 🎓 Credits

Built with:
- [face_recognition](https://github.com/ageitgey/face_recognition) by Adam Geitgey
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/) by Google
- [Gradio](https://gradio.app/)
- [dlib](http://dlib.net/)

---

**Made with ❤️ for privacy-conscious face recognition**

🚀 **Ready to get started?** Run `python app.py` and enjoy!
