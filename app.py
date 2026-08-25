import streamlit as st
import time  
from io import BytesIO
from PIL import Image
from rembg import remove
from cartooner import cartoonize
import cv2
import numpy as np

# Set up the Streamlit page
st.set_page_config(layout="wide", page_title="Image Cartoonizer")
st.title("🖼️ Image Cartoonizer")
st.write("This is an AI-powered image cartoonizer that applies cartoon effects and removes backgrounds.")

# Sidebar options
st.sidebar.write("## Upload Image & Customize :gear:")
my_upload = st.sidebar.file_uploader("Upload an image", type=["jpg", "png"])

alpha_matting = st.sidebar.checkbox("Use Alpha Matting", value=True)
threshold = st.sidebar.slider("Threshold", 0, 100, value=50, step=5)

cartoon_style = st.sidebar.selectbox("Choose Cartoon Style", ["Default", "Pencil Sketch", "Watercolor", "Oil Paint"])

# Function to convert PIL images to bytes for download
def convert_images(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# Function to remove background and apply cartoon effect
def process_image(uploaded_image, threshold, alpha_matting, cartoon_style):
    if uploaded_image is None:
        st.error("Please upload an image.")
        return

    # Show progress bar
    progress = st.progress(0)
    for i in range(101):
        time.sleep(0.01)
        progress.progress(i)

    # Open Image
    image = Image.open(uploaded_image)

    # Display Original Image
    col1, col2 = st.columns(2)
    col1.write("📸 **Original Image**")
    col1.image(image)

    # Remove Background
    col2.write("🎨 **Background Removed Image**")
    fixed = remove(image, alpha_matting=alpha_matting, alpha_matting_background_threshold=threshold)
    col2.image(fixed)

    st.success("✅ Image processed successfully!")

    # Convert to NumPy for OpenCV processing
    img_cv = np.array(image.convert("RGB"))  # Ensure it's in RGB format

    # Apply Cartoonization Based on User Choice
    if cartoon_style == "Default":
        cartoon = cartoonize(img_cv)
    elif cartoon_style == "Pencil Sketch":
        gray, sketch = cv2.pencilSketch(img_cv, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        cartoon = sketch
    elif cartoon_style == "Watercolor":
        cartoon = cv2.stylization(img_cv, sigma_s=60, sigma_r=0.6)
    elif cartoon_style == "Oil Paint":
       cartoon = cv2.stylization(img_cv, sigma_s=150, sigma_r=0.25)  # Simulates oil painting


    # Convert cartoonized image back to PIL format
    cartoon_pil = Image.fromarray(cartoon)
    st.write("🖌️ **Cartoonized Image**")
    st.image(cartoon_pil)

    # Download buttons
    st.sidebar.download_button("📥 Download Background Removed Image", data=convert_images(fixed), file_name="fixed_image.png")
    st.sidebar.download_button("📥 Download Cartoonized Image", data=convert_images(cartoon_pil), file_name="cartoonized_image.png")

# Load Default Image if No Upload
if my_upload:
    process_image(my_upload, threshold, alpha_matting, cartoon_style)
else:
    st.info("👆 Please upload an image to get started.")
    
