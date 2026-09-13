# 🔥 Fire & Smoke Detection System

A real-time **Fire and Smoke Detection System** powered by **YOLO11** and **Streamlit**.

This end-to-end Computer Vision application uses custom-trained YOLO11 weights to detect **fire** and **smoke** across multiple input sources, including images, videos, and live webcam streams.

The system also includes **low-light image enhancement, real-time performance controls, browser-compatible video processing, and automated email alerts**.

---

## 🚀 Video Demo
https://github.com/user-attachments/assets/27f18478-6ced-4087-9b68-d161c46659c9

---


## 🚀 View Screenshot
<img width="1888" height="810" alt="image" src="https://github.com/user-attachments/assets/7cb2d16a-12f0-4c28-9f6a-3aa64e001d94" />

---
## 🚀 Features

### 🔥 Real-Time Fire & Smoke Detection

The system uses a custom-trained **YOLO11 model** to detect:

- 🔥 Fire
- 💨 Smoke

Detection results include annotated bounding boxes and confidence scores.

---

### 📷 Image Detection

Upload an image and detect fire or smoke instantly.

**Supported formats:**

- `.jpg`
- `.jpeg`
- `.png`

The application displays:

- Original image
- Detection results
- Annotated bounding boxes
- Confidence scores

---

### 🎥 Video Detection

Upload a video and process it frame by frame using the YOLO11 detection model.

**Supported formats:**

- `.mp4`
- `.avi`
- `.mov`
- `.mkv`

Features include:

- Frame-by-frame detection
- Annotated detection results
- Progress indicators
- Processed video generation
- Browser-compatible MP4 output

The system uses `imageio` and `imageio-ffmpeg` to generate H.264-compatible videos that can be played directly in modern web browsers.

---

### 📹 Live Webcam Detection

The application supports continuous real-time monitoring using a webcam.

Features include:

- Real-time fire detection
- Real-time smoke detection
- Live annotated frames
- Frame-skipping controls
- Adjustable inference resolution
- Configurable confidence threshold

---

### 📧 Automated Email Alerts

When fire or smoke is detected during a live camera stream, the system can automatically send an emergency email alert.

The alert system:

- Captures a detection snapshot
- Converts the frame into a JPEG image
- Attaches the image to the email
- Sends automated alerts using Gmail SMTP
- Supports an optional custom recipient email

To prevent repeated notifications during continuous detection, the system includes a:

> ⏱️ **60-second alert cooldown mechanism**

This helps prevent unnecessary email flooding.

> ⚠️ Sensitive information such as email credentials should always be stored securely using Streamlit Secrets or environment variables.

---

## 🌙 Low-Light Image Enhancement

The system integrates **CLAHE (Contrast Limited Adaptive Histogram Equalization)** using OpenCV.

CLAHE improves image contrast and can help enhance visibility in:

- Low-light environments
- Dim areas
- Hazy scenes
- Reduced visibility conditions

This preprocessing step helps prepare images before model inference.

---

## ⚡ Performance Optimization

The application provides configurable controls to balance detection accuracy and real-time performance.

### Available Controls

- **Inference Resolution:** 320px – 640px
- **Frame Skipping**
- **Confidence Threshold**
- **CLAHE Low-Light Enhancement**

These controls allow users to optimize the system depending on:

- Hardware capabilities
- Processing speed
- Camera resolution
- Real-time monitoring requirements

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Model** | YOLO11 / Ultralytics | Fire and smoke object detection |
| **Frontend** | Streamlit | Interactive web application |
| **Computer Vision** | OpenCV | Image and video processing |
| **Image Processing** | Pillow, NumPy | Image manipulation |
| **Video Processing** | ImageIO, ImageIO-FFmpeg | Video encoding and export |
| **Email Alerts** | SMTP, Email MIME | Automated emergency notifications |
| **Programming Language** | Python | Core application development |

---

## 📦 Dependencies

Main dependencies include:

```text
ultralytics
streamlit
opencv-python-headless
numpy
pillow
imageio
imageio-ffmpeg
```

Install all required dependencies using:

```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```text
Fire-Detection/
│
├── .streamlit/
│   └── secrets.toml          # SMTP credentials and sensitive configuration
│
├── weights/
│   └── best.pt               # Custom-trained YOLO11 model weights
│
├── app.py                    # Main Streamlit application and inference logic
│
├── requirements.txt          # Project dependencies
│
├── .gitignore                # Ignored files and sensitive configurations
│
└── README.md                 # Project documentation
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

### 2. Navigate to the Project Directory

```bash
cd Fire-Detection
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will automatically open in your browser.

---

## 🔐 Email Configuration

To enable automated email alerts, configure your SMTP credentials securely.

Example `.streamlit/secrets.toml`:

```toml
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
```

> ⚠️ Never upload your email password, app password, API keys, or other sensitive credentials to GitHub.

Make sure the following file is included in `.gitignore`:

```text
.streamlit/secrets.toml
```

For Gmail, it is recommended to use an **App Password** instead of your primary account password.

---

## 🧠 System Workflow

```text
Input Source
     │
     ▼
Image / Video / Webcam
     │
     ▼
Preprocessing
     │
     ├── CLAHE Enhancement
     │
     ▼
YOLO11 Inference
     │
     ▼
Fire / Smoke Detection
     │
     ├── Bounding Boxes
     ├── Confidence Scores
     │
     ▼
Detection Result
     │
     ├── Display Results
     ├── Save Processed Video
     └── Send Email Alert
```

---

## 🎯 Use Cases

This system can potentially be adapted for:

- 🏭 Industrial safety monitoring
- 🏢 Building surveillance
- 🏠 Smart home safety systems
- 🌲 Forest fire monitoring
- 🚗 Vehicle safety systems
- 🏗️ Construction site monitoring
- 🔥 Early fire detection research

---

## 🔮 Future Improvements

Possible future improvements include:

- Multi-camera monitoring
- Cloud deployment
- SMS alerts
- WhatsApp notifications
- IoT sensor integration
- Fire severity estimation
- Detection history dashboard
- Database integration
- Cloud storage for detection snapshots
- Mobile application integration
- Edge device optimization

---

## 🧠 Built With

- Python
- YOLO11
- Ultralytics
- Streamlit
- OpenCV
- NumPy
- Pillow
- ImageIO
- SMTP

---

## 📄 License

This project is intended for **educational and research purposes**.

---

## 👨‍💻 Author

**Yasir Baig**  
AI Engineer | Machine Learning | Computer Vision

⭐ If you found this project useful, consider giving the repository a star!
