# FIre-Detection
Real-time Fire and smoke detection using yolov11n.pt
# ⚙️ Real-Time Smoke & Fire Detection System

An end-to-end Computer Vision system designed to detect fire and smoke in real time. Built with custom-trained **YOLO11** weights and a responsive **Streamlit** dashboard, the application handles image analysis, video file processing, continuous webcam streams, and automated emergency notification dispatch.

🚀 **Live Interactive Demo:** [fire-detection-gabr.streamlit.app](https://fire-detection-gabr.streamlit.app/)      
    **Linkedin Post:** [Fire detection project post] (https://lnkd.in/p/eQQpQ-eu)

---

## 📌 Key Highlights

* **Multi-Input Inference:** Seamlessly switch between static image inspection, video file batch processing, and live webcam feeds.
* **H.264 Web-Compatible Video Processing:** Uses `imageio` with embedded FFmpeg encoding to write `.mp4` video files directly streamable inside modern web browsers.
* **Automated SMTP Email Alerts:** Sends direct JPEG snapshot attachments via Gmail SMTP when fire/smoke is detected on live streams.
* **Real-time Performance Optimization:** Includes dynamic resolution scaling ($320\text{px}$ to $640\text{px}$), frame-skipping controls, and CLAHE (Contrast Limited Adaptive Histogram Equalization) image enhancement for low-light environments.

---

## 🛠️ Tech Stack & Dependencies

| Layer | Component / Library | Purpose |
| :--- | :--- | :--- |
| **Model** | `ultralytics` (YOLO11) | Object detection for `fire` and `smoke` classes |
| **Frontend** | `streamlit` | Interactive GUI, sidebar configuration, and media display |
| **Vision & Image** | `opencv-python-headless`, `pillow`, `numpy` | Image decoding, color transformation, CLAHE preprocessing |
| **Video Processing**| `imageio`, `imageio-ffmpeg` | Frame-by-frame annotation and H.264 MP4 export |
| **Alert Systems** | `smtplib`, `email.mime` | Secure background email dispatch with image attachments |

---

## ✨ System Features & Interface

### 📷 1. Image Detection
Upload `.jpg`, `.jpeg`, or `.png` files to view side-by-side comparisons of the raw input and annotated bounding-box predictions.

### 🎥 2. Video File Processing
Upload pre-recorded media (`.mp4`, `.avi`, `.mov`, `.mkv`). The video is processed frame-by-frame with active progress indicators and rendered natively for browser playback upon completion.

### 📹 3. Live Camera Feed & Automated Email Dispatch
Run continuous webcam monitoring with dynamic frame skipping.
> ⚠️ **Alert System Behavior:**
> * When **Enable Automatic Email Alerts** is checked, detecting fire or smoke triggers an automated alert email.
> * The alert includes a JPEG frame snapshot attached directly to the message.
> * Alerts are dispatched to the primary target **`abdogabr688@gmail.com`** and any optional custom email address specified in the sidebar.
> * Includes a **60-second cooldown timer** to prevent email spamming during continuous detection.

---

## 📁 Repository Architecture

```text
Fire-Detection/
├── .streamlit/
│   └── secrets.toml          # Encrypted local SMTP credentials (git-ignored)
├── weights/
│   └── best.pt               # Trained YOLO11 model weights file
├── app.py                    # Main Streamlit web application & inference logic
├── requirements.txt          # Python runtime dependencies for Streamlit Cloud
├── .gitignore                # Excludes virtual environments and sensitive files
└── README.md                 # Project documentation
