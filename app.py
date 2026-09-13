import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import time
import smtplib
from PIL import Image
from ultralytics import YOLO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# --- 1. EMAIL DISPATCH FUNCTION ---
def send_fire_alert_email(image_bgr, recipient_list):
    sender_email = "n8ngabr@gmail.com"
    sender_app_password = "zlki ovnb ymcl mqhn"

    valid_recipients = [e.strip() for e in recipient_list if e and e.strip()]
    if not valid_recipients:
        return False

    subject = "🚨 ALERT: Fire Detected on Live Camera Stream!"
    body = "Fire or smoke was detected during live camera monitoring. The captured snapshot is attached below."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(valid_recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    is_success, buffer = cv2.imencode(".jpg", image_bgr)
    if is_success:
        image_attachment = MIMEImage(buffer.tobytes(), name="fire_alert.jpg")
        msg.attach(image_attachment)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_app_password)
        server.sendmail(sender_email, valid_recipients, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email alert: {e}")
        return False

# --- 2. PAGE CONFIG & TITLE ---
st.set_page_config(
    page_title="Fire Detection YOLO11 | Mirza Yasir Abdullah Baig",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 Fire Detection YOLO11 by Mirza Yasir Abdullah Baig")
st.caption("Real-Time Smoke & Fire Detection System powered by YOLO11")

# --- 3. SIDEBAR: ABOUT SECTION ---
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        **Fire Detection YOLO11**  
        Developed by **Mirza Yasir Abdullah Baig**

        A real-time smoke and fire detection system built with
        YOLO11, OpenCV, and Streamlit — supporting image, video,
        and live camera stream inference with automatic email alerts.

        🔗 [GitHub](https://github.com/mirzayasirabdullahbaig07)  
        🔗 [LinkedIn](https://www.linkedin.com/in/mirza-yasir-abdullah-baig/)
        """
    )
    st.divider()

# --- 4. SIDEBAR NAVIGATION & PARAMETERS ---
st.sidebar.header("Navigation")
input_mode = st.sidebar.radio("Select Input Mode", ["Image", "Video", "Live Camera Feed"])

st.sidebar.header("Inference Settings")
conf_threshold = st.sidebar.slider("Confidence Threshold", 0.1, 1.0, 0.25, 0.05)
apply_clahe = st.sidebar.checkbox("Apply CLAHE Preprocessing", value=True)

# Performance Tuning Settings
st.sidebar.header("Performance Settings")
frame_skip = st.sidebar.slider("Frame Skip (Higher = Slower)", 1, 20, 2)
img_size = st.sidebar.select_slider("Inference Resolution", options=[320, 480, 640], value=480)

# Helper function for CLAHE
def preprocess_frame(img):
    if apply_clahe:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge((l, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return img

# --- 5. LOAD MODEL ---
@st.cache_resource
def load_model():
    return YOLO('weights/best.pt')

model = load_model()

# --- MODE 1: IMAGE ---
if input_mode == "Image":
    st.subheader("📷 Image Detection")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        processed_image = preprocess_frame(image.copy())

        with st.spinner("Running Detection..."):
            results = model.predict(source=processed_image, conf=conf_threshold, imgsz=img_size)

        annotated_frame = cv2.cvtColor(results[0].plot(), cv2.COLOR_BGR2RGB)

        col1, col2 = st.columns(2)
        with col1:
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Original Image", use_container_width=True)
        with col2:
            st.image(annotated_frame, caption="Detection Output", use_container_width=True)

# --- MODE 2: VIDEO ---
elif input_mode == "Video":
    st.subheader("🎥 Video File Detection")
    uploaded_video = st.file_uploader("Upload a video...", type=["mp4", "avi", "mov", "mkv"])

    if uploaded_video is not None:
        import imageio

        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_video.read())
        tfile.close()

        cap = cv2.VideoCapture(tfile.name)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

        output_path = tempfile.NamedTemporaryFile(delete=False, suffix='_h264.mp4').name
        writer = imageio.get_writer(output_path, fps=fps, codec='libx264', format='FFMPEG')

        progress_bar = st.progress(0)
        status_text = st.empty()
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        frame_count = 0
        last_annotated_rgb = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            if frame_count % frame_skip == 0 or last_annotated_rgb is None:
                processed_frame = preprocess_frame(frame.copy())
                results = model.predict(source=processed_frame, conf=conf_threshold, imgsz=img_size, verbose=False)
                last_annotated_rgb = cv2.cvtColor(results[0].plot(), cv2.COLOR_BGR2RGB)

            writer.append_data(last_annotated_rgb)

            if total_frames > 0:
                progress_bar.progress(min(frame_count / total_frames, 1.0))
                status_text.text(f"Processing frame {frame_count}/{total_frames}...")

        cap.release()
        writer.close()

        status_text.success("Processing complete! Rendering video playback...")

        with open(output_path, 'rb') as video_file:
            st.video(video_file.read())

# --- MODE 3: LIVE CAMERA FEED ---
elif input_mode == "Live Camera Feed":
    st.subheader("📹 Real-Time Continuous Camera Stream")

    # Sidebar Notification Controls
    st.sidebar.header("Email Alert Options")
    enable_email_alerts = st.sidebar.checkbox("Enable Automatic Email Alerts", value=False)
    custom_user_email = st.sidebar.text_input("Additional Target Email (Optional):", placeholder="user@example.com")

    run_cam = st.checkbox("Start Camera Stream")
    st_frame = st.empty()

    if "last_email_time" not in st.session_state:
        st.session_state.last_email_time = 0

    if run_cam:
        cap = cv2.VideoCapture(0)

        frame_count = 0
        last_annotated_frame = None

        while cap.isOpened() and run_cam:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to access webcam.")
                break

            frame_count += 1

            if frame_count % frame_skip == 0 or last_annotated_frame is None:
                processed_frame = preprocess_frame(frame.copy())
                results = model.predict(source=processed_frame, conf=conf_threshold, imgsz=img_size, verbose=False)

                annotated_bgr = results[0].plot()
                last_annotated_frame = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)

                # Send email ONLY if the toggle switch is ACTIVE and detections exist
                boxes = results[0].boxes
                if len(boxes) > 0 and enable_email_alerts:
                    current_time = time.time()
                    if current_time - st.session_state.last_email_time > 60:
                        st.toast("🚨 Fire detected! Sending alert email...", icon="🔥")

                        recipients = ["abdogabr688@gmail.com"]
                        if custom_user_email:
                            recipients.append(custom_user_email)

                        success = send_fire_alert_email(annotated_bgr, recipients)
                        if success:
                            st.session_state.last_email_time = current_time
                            st.sidebar.success("Alert email sent successfully!")

            st_frame.image(last_annotated_frame, caption="Live Webcam Detection", use_container_width=True)

        cap.release()

# --- FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
        Built with ❤️ by <b>Mirza Yasir Abdullah Baig</b> ·
        <a href="https://github.com/mirzayasirabdullahbaig07" target="_blank">GitHub</a> ·
        <a href="https://www.linkedin.com/in/mirza-yasir-abdullah-baig/" target="_blank">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True
)