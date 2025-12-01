"""
Face Recognition System - Perfect User Flow
Real auto-capture + Smart registration + Admin panel
"""
import cv2
import numpy as np
import gradio as gr
import os
import json
from datetime import datetime
import warnings
import logging
import time
import asyncio

# Suppress warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
logging.getLogger("asyncio").setLevel(logging.ERROR)

# Database Manager
class FaceDatabase:
    def __init__(self, db_path: str = "faces.json"):
        self.db_path = db_path
        self.data = self.load_database()
    
    def load_database(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {"users": []}
    
    def save_database(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_user(self, name: str, image_path: str, features: dict):
        # Remove existing user if present (and delete old image)
        existing_user = next((u for u in self.data["users"] if u["name"].lower() == name.lower()), None)
        if existing_user and os.path.exists(existing_user["image"]):
            try:
                os.remove(existing_user["image"])
            except:
                pass
        
        self.data["users"] = [u for u in self.data["users"] if u["name"].lower() != name.lower()]
        
        # Add new user with pre-computed features
        self.data["users"].append({
            "name": name,
            "image": image_path,
            "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "features": {
                "lbp_hist": features["lbp_hist"].tolist(),
                "hog_hist": features["hog_hist"].tolist(),
                "color_hist": features["color_hist"].tolist(),
                "gray_hist": features["gray_hist"].tolist(),
                "edges_hist": features["edges_hist"].tolist()
            }
        })
        self.save_database()
    
    def delete_user(self, name: str):
        user = next((u for u in self.data["users"] if u["name"] == name), None)
        if user and os.path.exists(user["image"]):
            os.remove(user["image"])
        self.data["users"] = [u for u in self.data["users"] if u["name"] != name]
        self.save_database()
    
    def get_all_users(self):
        # Reload database to get fresh data
        self.data = self.load_database()
        return [(u["name"], u.get("registered_at", "Unknown"), u["image"]) for u in self.data["users"]]

# Initialize
db = FaceDatabase()
FACES_DIR = "faces"
os.makedirs(FACES_DIR, exist_ok=True)

def detect_face(image):
    """Advanced face detection"""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Primary detection
    faces = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(120, 120),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    # Fallback detection
    if len(faces) == 0:
        faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(100, 100))
    
    return faces

def extract_advanced_features(face_img):
    """Extract comprehensive facial features"""
    face_img = cv2.resize(face_img, (160, 160))
    gray = cv2.cvtColor(face_img, cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    
    features = {}
    
    # 1. LBP
    def compute_lbp(img, radius=1):
        lbp = np.zeros_like(img, dtype=np.uint8)
        for i in range(radius, img.shape[0]-radius):
            for j in range(radius, img.shape[1]-radius):
                center = img[i, j]
                code = 0
                points = [
                    (i-radius, j-radius), (i-radius, j), (i-radius, j+radius),
                    (i, j+radius), (i+radius, j+radius), (i+radius, j),
                    (i+radius, j-radius), (i, j-radius)
                ]
                for idx, (pi, pj) in enumerate(points):
                    if img[pi, pj] >= center:
                        code |= (1 << idx)
                lbp[i, j] = code
        return lbp
    
    lbp1 = compute_lbp(denoised, 1)
    lbp2 = compute_lbp(denoised, 2)
    hist_lbp1 = cv2.calcHist([lbp1], [0], None, [256], [0, 256])
    hist_lbp2 = cv2.calcHist([lbp2], [0], None, [256], [0, 256])
    features['lbp_hist'] = np.concatenate([hist_lbp1.flatten(), hist_lbp2.flatten()])
    features['lbp_hist'] = features['lbp_hist'] / (np.sum(features['lbp_hist']) + 1e-7)
    
    # 2. HOG
    gx = cv2.Sobel(denoised, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(denoised, cv2.CV_32F, 0, 1, ksize=3)
    mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
    bins = 36
    hog_hist = np.zeros(bins)
    for i in range(angle.shape[0]):
        for j in range(angle.shape[1]):
            bin_idx = int(angle[i, j] / (360.0 / bins)) % bins
            hog_hist[bin_idx] += mag[i, j]
    features['hog_hist'] = hog_hist / (np.sum(hog_hist) + 1e-7)
    
    # 3. Color
    hsv = cv2.cvtColor(face_img, cv2.COLOR_RGB2HSV)
    h, w = hsv.shape[:2]
    regions = [
        hsv[0:h//2, 0:w//2], hsv[0:h//2, w//2:w],
        hsv[h//2:h, 0:w//2], hsv[h//2:h, w//2:w], hsv
    ]
    color_hists = []
    for region in regions:
        hist_h = cv2.calcHist([region], [0], None, [16], [0, 180])
        hist_s = cv2.calcHist([region], [1], None, [16], [0, 256])
        color_hists.extend([hist_h.flatten(), hist_s.flatten()])
    features['color_hist'] = np.concatenate(color_hists)
    features['color_hist'] = features['color_hist'] / (np.sum(features['color_hist']) + 1e-7)
    
    # 4. Gray
    gray_regions = [
        gray[0:h//2, 0:w//2], gray[0:h//2, w//2:w],
        gray[h//2:h, 0:w//2], gray[h//2:h, w//2:w], gray
    ]
    gray_hists = []
    for region in gray_regions:
        hist = cv2.calcHist([region], [0], None, [32], [0, 256])
        gray_hists.append(hist.flatten())
    features['gray_hist'] = np.concatenate(gray_hists)
    features['gray_hist'] = features['gray_hist'] / (np.sum(features['gray_hist']) + 1e-7)
    
    # 5. Edges
    edges = cv2.Canny(denoised, 50, 150)
    edge_regions = [
        edges[0:h//2, 0:w//2], edges[0:h//2, w//2:w],
        edges[h//2:h, 0:w//2], edges[h//2:h, w//2:w]
    ]
    edge_densities = [np.sum(region > 0) / region.size for region in edge_regions]
    edge_hist = cv2.calcHist([edges], [0], None, [32], [0, 256])
    features['edges_hist'] = np.concatenate([edge_hist.flatten(), edge_densities])
    features['edges_hist'] = features['edges_hist'] / (np.sum(features['edges_hist']) + 1e-7)
    features['face_normalized'] = denoised
    
    return features

def compare_advanced_features(feat1, feat2):
    """Compare features"""
    scores = []
    
    lbp_corr = np.corrcoef(feat1['lbp_hist'], feat2['lbp_hist'])[0, 1]
    lbp_chi = cv2.compareHist(
        feat1['lbp_hist'].astype(np.float32).reshape(-1, 1),
        feat2['lbp_hist'].astype(np.float32).reshape(-1, 1),
        cv2.HISTCMP_CHISQR
    )
    lbp_score = (lbp_corr + (1 - min(lbp_chi / 100, 1))) / 2
    scores.append(lbp_score * 0.30)
    
    hog_corr = np.corrcoef(feat1['hog_hist'], feat2['hog_hist'])[0, 1]
    scores.append(max(0, hog_corr) * 0.25)
    
    color_corr = np.corrcoef(feat1['color_hist'], feat2['color_hist'])[0, 1]
    scores.append(max(0, color_corr) * 0.15)
    
    gray_corr = np.corrcoef(feat1['gray_hist'], feat2['gray_hist'])[0, 1]
    scores.append(max(0, gray_corr) * 0.10)
    
    edges_corr = np.corrcoef(feat1['edges_hist'], feat2['edges_hist'])[0, 1]
    scores.append(max(0, edges_corr) * 0.10)
    
    result = cv2.matchTemplate(
        feat1['face_normalized'],
        feat2['face_normalized'],
        cv2.TM_CCOEFF_NORMED
    )
    template_score = max(0, result[0][0])
    scores.append(template_score * 0.10)
    
    final_score = sum(scores)
    return min(max(final_score, 0), 1)

def verify_user_auto(image):
    """Auto-verify after capture with quality checks"""
    if image is None:
        return "⏳ Waiting for capture...", None, gr.update(visible=False), gr.update(visible=False), ""
    
    # Enhance image quality
    enhanced_image = enhance_image_quality(image)
    
    # Detect face
    faces = detect_face(enhanced_image)
    
    if len(faces) == 0:
        return "❌ **NO FACE DETECTED**\n\n💡 Please:\n• Face camera directly\n• Better lighting\n• Position in green guide", None, gr.update(visible=True), gr.update(visible=False), "✅ Ready for capture"
    
    if len(faces) > 1:
        return "❌ **MULTIPLE FACES**\n\nOnly one person should be visible.", None, gr.update(visible=True), gr.update(visible=False), "✅ Ready for capture"
    
    # Extract face
    (x, y, w, h) = faces[0]
    face_img = enhanced_image[y:y+h, x:x+w]
    
    # Check face size (quality)
    if w < 150 or h < 150:
        return "❌ **FACE TOO SMALL**\n\nPlease move closer to camera", None, gr.update(visible=True), gr.update(visible=False), f"⚠️ Face Size: {w}x{h} (Need >150x150)"
    
    # Reload database to get latest users
    db.data = db.load_database()
    
    # Check database
    if len(db.data["users"]) == 0:
        return "❓ **NO USERS IN DATABASE**\n\nWould you like to register?", None, gr.update(visible=False), gr.update(visible=True), "✅ Image Quality: Good"
    
    # Extract features
    try:
        captured_features = extract_advanced_features(face_img)
    except Exception as e:
        return f"❌ Error: {str(e)}", None, gr.update(visible=True), gr.update(visible=False), "⚠️ Processing Error"
    
    # Compare with all users
    best_match = None
    best_score = 0
    all_scores = []
    
    for user in db.data["users"]:
        try:
            stored_features = {
                'lbp_hist': np.array(user['features']['lbp_hist']),
                'hog_hist': np.array(user['features']['hog_hist']),
                'color_hist': np.array(user['features']['color_hist']),
                'gray_hist': np.array(user['features']['gray_hist']),
                'edges_hist': np.array(user['features']['edges_hist'])
            }
            
            if os.path.exists(user['image']):
                stored_img = cv2.imread(user['image'])
                stored_img = cv2.cvtColor(stored_img, cv2.COLOR_BGR2RGB)
                
                # Enhance stored image too
                stored_img = enhance_image_quality(stored_img)
                
                stored_faces = detect_face(stored_img)
                
                if len(stored_faces) > 0:
                    (sx, sy, sw, sh) = stored_faces[0]
                    stored_face = stored_img[sy:sy+sh, sx:sx+sw]
                    stored_face_resized = cv2.resize(stored_face, (160, 160))
                    stored_gray = cv2.cvtColor(stored_face_resized, cv2.COLOR_RGB2GRAY)
                    stored_gray = cv2.equalizeHist(stored_gray)
                    stored_gray = cv2.fastNlMeansDenoising(stored_gray, None, 10, 7, 21)
                    stored_features['face_normalized'] = stored_gray
                else:
                    continue
            else:
                continue
            
            score = compare_advanced_features(captured_features, stored_features)
            all_scores.append((user["name"], score))
            
            if score > best_score:
                best_score = score
                best_match = user["name"]
        
        except Exception as e:
            print(f"Error comparing with {user['name']}: {e}")
            continue
    
    BASE_THRESHOLD = 0.60  # Lowered from 0.68 for better recognition
    
    if best_score >= BASE_THRESHOLD:
        confidence = best_score * 100
        
        if len(all_scores) >= 2:
            sorted_scores = sorted(all_scores, key=lambda x: x[1], reverse=True)
            gap = sorted_scores[0][1] - sorted_scores[1][1]
            
            if gap < 0.05:
                return f"⚠️ **UNCERTAIN**\n\nBest: {best_match} ({confidence:.1f}%)\nToo close to call.", None, gr.update(visible=False), gr.update(visible=False), "✅ Verification Complete"
        
        return f"✅ **ACCESS GRANTED**\n\n🎉 Welcome, **{best_match}**!\n\n📊 Confidence: {confidence:.1f}%", best_match, gr.update(visible=False), gr.update(visible=False), f"✅ Verified Successfully"
    
    else:
        if all_scores:
            top_matches = sorted(all_scores, key=lambda x: x[1], reverse=True)[:2]
            details = "\n".join([f"  • {name}: {score*100:.1f}%" for name, score in top_matches])
            return f"❌ **NOT RECOGNIZED**\n\n📊 Best matches:\n{details}\n\n🔒 Required: {BASE_THRESHOLD*100:.0f}%", None, gr.update(visible=True), gr.update(visible=True), f"✅ Image Quality: Good"
        else:
            return "❌ **NO MATCH**", None, gr.update(visible=True), gr.update(visible=True), "✅ Ready for capture"

def register_user(name, image):
    """Register new user"""
    if not name or name.strip() == "":
        return "❌ Please enter a name.", gr.update()
    
    if image is None:
        return "❌ No image captured.", gr.update()
    
    name = name.strip()
    faces = detect_face(image)
    
    if len(faces) == 0:
        return "❌ **NO FACE DETECTED**", gr.update()
    
    if len(faces) > 1:
        return "❌ **MULTIPLE FACES**", gr.update()
    
    (x, y, w, h) = faces[0]
    face_img = image[y:y+h, x:x+w]
    
    if w < 120 or h < 120:
        return "❌ **FACE TOO SMALL**", gr.update()
    
    try:
        features = extract_advanced_features(face_img)
    except Exception as e:
        return f"❌ Error: {str(e)}", gr.update()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name.replace(' ', '_')}_{timestamp}.jpg"
    filepath = os.path.join(FACES_DIR, filename)
    
    img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filepath, img_bgr)
    
    db.add_user(name, filepath, features)
    
    return f"✅ **REGISTERED!**\n\n👤 {name}\n📸 Saved successfully\n\n🔐 You can now verify!", gr.update(visible=False)

def get_users_list():
    """Get formatted users list for admin"""
    users = db.get_all_users()
    if not users:
        return "No users registered yet."
    
    output = f"**📋 Registered Users ({len(users)}):**\n\n"
    for i, (name, reg_time, img_path) in enumerate(users, 1):
        output += f"{i}. **{name}**\n   📅 Registered: {reg_time}\n\n"
    return output

def delete_user_func(name):
    """Delete user from admin panel"""
    if not name:
        return "❌ Please enter a name to delete.", gr.update()
    
    user = next((u for u in db.data["users"] if u["name"] == name), None)
    if not user:
        return f"❌ User '{name}' not found.", gr.update()
    
    db.delete_user(name)
    return f"✅ User '{name}' deleted successfully.", get_users_list()

# Auto-capture state
auto_capture_active = False

def stream_feedback(image):
    """Provide real-time feedback on camera stream"""
    if image is None:
        return "💡 Waiting for camera..."
    
    # Enhance image quality
    enhanced_image = enhance_image_quality(image)
    
    # Detect face
    faces = detect_face(enhanced_image)
    
    if len(faces) == 0:
        return "❌ No face detected - Position yourself in frame"
    
    if len(faces) > 1:
        return "⚠️ Multiple faces detected - Only one person should be visible"
    
    # Extract face
    (x, y, w, h) = faces[0]
    
    # Check face size
    if w < 150 or h < 150:
        return f"⚠️ Face too small ({w}x{h}) - Move closer to camera"
    
    # Check blur
    face_img = enhanced_image[y:y+h, x:x+w]
    gray_face = cv2.cvtColor(face_img, cv2.COLOR_RGB2GRAY)
    blur_score = cv2.Laplacian(gray_face, cv2.CV_64F).var()
    
    if blur_score < 100:
        return f"⚠️ Image blurry (score: {blur_score:.0f}) - Hold still"
    
    # Check brightness
    brightness = np.mean(gray_face)
    if brightness < 60:
        return "⚠️ Too dark - Improve lighting"
    if brightness > 200:
        return "⚠️ Too bright - Reduce lighting"
    
    # All checks passed
    return f"✅ Face detected! Good quality - Click 'Capture & Verify' (Face: {w}x{h}, Clarity: {blur_score:.0f})"

def detect_blur(image):
    """Detect if image is blurry using Laplacian variance"""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var

def enhance_image_quality(image):
    """Enhance image for better recognition"""
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Merge channels
    enhanced_lab = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
    
    # Denoise
    enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
    
    # Sharpen
    kernel = np.array([[-1,-1,-1],
                       [-1, 9,-1],
                       [-1,-1,-1]])
    enhanced = cv2.filter2D(enhanced, -1, kernel)
    
    return enhanced

# Create Gradio Interface
with gr.Blocks(title="Face Recognition", theme=gr.themes.Soft(), css="""
    .big-button { 
        font-size: 18px !important; 
        padding: 20px !important; 
    }
    /* Face guide overlay */
    [data-testid="image"] {
        position: relative !important;
    }
    [data-testid="image"]::before {
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 220px !important;
        height: 280px !important;
        border: 5px solid #00ff00 !important;
        border-radius: 50% !important;
        pointer-events: none !important;
        z-index: 999 !important;
        box-shadow: 
            inset 0 0 30px rgba(0, 255, 0, 0.4),
            0 0 40px rgba(0, 255, 0, 0.6) !important;
        animation: pulse-guide 2s ease-in-out infinite !important;
    }
    @keyframes pulse-guide {
        0%, 100% { 
            border-color: #00ff00 !important;
            opacity: 1 !important;
        }
        50% { 
            border-color: #00ff88 !important;
            opacity: 0.8 !important;
        }
    }
    .status-good { color: #00ff00; font-weight: bold; }
    .status-bad { color: #ff0000; font-weight: bold; }
""") as app:
    
    gr.Markdown("""
    # 🔐 Face Recognition System
    ### Smart verification with auto-capture
    """)
    
    with gr.Tabs() as tabs:
        # USER VERIFICATION TAB
        with gr.Tab("👤 Verify Identity"):
            gr.Markdown("### 🎯 Automatic Face Verification")
            gr.Markdown("**Camera will auto-capture when your face is detected and properly aligned!**")
            
            with gr.Row():
                with gr.Column(scale=1):
                    user_camera = gr.Image(
                        sources=["webcam"],
                        type="numpy",
                        label="📸 Position your face in the green oval guide",
                        streaming=True,
                        mirror_webcam=False
                    )
                    
                    capture_btn = gr.Button("🎯 Capture & Verify", variant="primary", size="lg", elem_classes=["big-button"])
                    
                    quality_status = gr.Markdown("💡 **Tip:** Click 'Capture & Verify' when your face is aligned", elem_classes=["status-good"])
                
                with gr.Column(scale=1):
                    result_box = gr.Markdown("", label="Result")
                    matched_name = gr.Textbox(visible=False)
                    
                    with gr.Column(visible=False) as retry_box:
                        gr.Markdown("### 🔄 Want to try again?")
                        retry_btn = gr.Button("Try Again", variant="secondary", size="lg")
                    
                    with gr.Column(visible=False) as register_box:
                        gr.Markdown("### 📝 Not Registered? Register Now!")
                        reg_name_input = gr.Textbox(
                            label="Enter Your Full Name",
                            placeholder="e.g., John Smith"
                        )
                        reg_btn = gr.Button("✅ Register Me", variant="primary", size="lg")
                        reg_result = gr.Markdown("")
            
            gr.Markdown("""
            ---
            **💡 How It Works:**
            1. **Allow camera access** when prompted
            2. **Align your face** in the glowing green oval guide
            3. **Click "Capture & Verify"** button when ready
            4. **Instant verification** - Result appears automatically
            5. If not found, you can register on the spot!
            
            **✨ Quality Tips:**
            - Bright, even lighting (no shadows)
            - Face camera directly (not at angle)
            - Remove glasses if possible
            - Remove glasses if possible
            - Neutral expression works best
            """)
        
        # ADMIN PANEL TAB
        with gr.Tab("⚙️ Admin Panel"):
            gr.Markdown("### 🔧 Manage Registered Users")
            
            with gr.Row():
                with gr.Column():
                    users_display = gr.Markdown(value=get_users_list())
                    refresh_btn = gr.Button("🔄 Refresh List", variant="secondary")
                
                with gr.Column():
                    gr.Markdown("### ➖ Delete User")
                    delete_name = gr.Textbox(
                        label="User Name to Delete",
                        placeholder="Enter exact name"
                    )
                    delete_btn = gr.Button("🗑️ Delete User", variant="stop")
                    delete_result = gr.Markdown("")
    
    # Event Handlers
    # Real-time feedback on camera stream
    user_camera.stream(
        fn=stream_feedback,
        inputs=[user_camera],
        outputs=[quality_status],
        show_progress=False
    )
    
    # Capture button triggers verification
    capture_btn.click(
        fn=verify_user_auto,
        inputs=[user_camera],
        outputs=[result_box, matched_name, retry_box, register_box, quality_status]
    )
    
    retry_btn.click(
        fn=lambda: ("✨ **Ready!** Position your face in the green guide.", None, gr.update(visible=False), gr.update(visible=False), "💡 Waiting for face..."),
        outputs=[result_box, matched_name, retry_box, register_box, quality_status]
    )
    
    reg_btn.click(
        fn=register_user,
        inputs=[reg_name_input, user_camera],
        outputs=[reg_result, register_box]
    )
    
    refresh_btn.click(
        fn=get_users_list,
        outputs=[users_display]
    )
    
    delete_btn.click(
        fn=delete_user_func,
        inputs=[delete_name],
        outputs=[delete_result, users_display]
    )

if __name__ == "__main__":
    print("=" * 60)
    print("🔐 FACE RECOGNITION SYSTEM")
    print("=" * 60)
    print("✅ Real-time camera feedback")
    print("✅ Smart user flow (verify → register)")
    print("✅ Admin panel with user management")
    print("=" * 60)
    print("🌐 Starting...")
    print("🏠 http://127.0.0.1:7860")
    print("=" * 60)
    
    app.launch(
        server_name="127.0.0.1", 
        server_port=7860,
        inbrowser=True,
        show_error=True
    )
