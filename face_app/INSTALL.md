# 🚀 Quick Installation Guide

## Windows Installation

### Step 1: Prerequisites
Make sure you have:
- ✅ Python 3.9 or higher installed
- ✅ A working webcam
- ✅ Internet connection (for initial setup)

Check Python version:
```powershell
python --version
```

### Step 2: Download Project
Download and extract this project to your desired location.

### Step 3: Install Dependencies

**Option A: Automatic (Recommended)**
```powershell
# Just double-click: run_app.bat
```
This will automatically:
- Create virtual environment
- Install all dependencies
- Start the application

**Option B: Manual**
```powershell
# Navigate to project folder
cd "path\to\face_app"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### Step 4: Run the Application

**Option A: Using Batch File**
```powershell
# Double-click run_app.bat
```

**Option B: Using Python**
```powershell
# Activate venv first
.\venv\Scripts\Activate.ps1

# Run app
python app_perfect.py
```

### Step 5: Access the Web Interface

Open your browser and go to:
```
http://127.0.0.1:7860
```

## 🛠️ Troubleshooting

### Python Not Found
Install Python from: https://www.python.org/downloads/

Make sure to check "Add Python to PATH" during installation.

### PowerShell Execution Policy Error
Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Module Not Found
Reinstall dependencies:
```powershell
pip install --upgrade -r requirements.txt
```

### Port 7860 Already in Use
Either:
1. Close the app using that port
2. Or change the port in `app_perfect.py`:
   ```python
   app.launch(server_name="0.0.0.0", server_port=7861)  # Change to 7861
   ```

## 📦 What Gets Installed

- **opencv-python** (4.12.0.88) - Face detection and image processing
- **numpy** (1.26.4) - Numerical computations
- **gradio** (4.19.2) - Web interface framework

Total download size: ~150MB
Installation time: 2-5 minutes

## ✅ Verify Installation

After installation, you should see:
```
Running on local URL:  http://0.0.0.0:7860
```

## 🎯 First Time Setup

1. **Register Yourself**
   - Click "Capture & Verify"
   - Click "Register Me"
   - Enter your name
   - Done!

2. **Test Recognition**
   - Click "Capture & Verify" again
   - Should recognize you!

## 🌐 Public Access (Optional)

To share your app publicly:

1. **Install ngrok**
   Download from: https://ngrok.com/download

2. **Run ngrok**
   ```powershell
   ngrok http 7860
   ```

3. **Share the URL**
   Copy the https URL and share it!

## 📞 Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review error messages carefully
- Make sure camera permissions are allowed
- Try restarting the application

## 🔄 Updating

To update dependencies:
```powershell
pip install --upgrade -r requirements.txt
```

---

**Ready to go! 🎉**

Now run the app and start using face recognition!
