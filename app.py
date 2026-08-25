import streamlit as st
from io import BytesIO
from PIL import Image
from rembg import remove
from cartooner import cartoonize
import cv2
import numpy as np

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Toonify AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>

/* ---------- MAIN APP ---------- */

.stApp {
    background:
        radial-gradient(circle at 15% 15%, rgba(255, 126, 210, 0.18), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(120, 150, 255, 0.20), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(170, 90, 255, 0.16), transparent 35%),
        linear-gradient(135deg, #090b22 0%, #101337 45%, #17102f 100%);
    color: #f7f5ff;
}

/* ---------- HIDE DEFAULT STREAMLIT UI ---------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* ---------- ANIMATED BACKGROUND ---------- */

.anime-bg {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}

/* glowing moon */
.moon {
    position: absolute;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    right: 7%;
    top: 8%;
    background:
        radial-gradient(circle at 35% 35%,
        #ffffff 0%,
        #eee8ff 35%,
        #c9c2ff 65%,
        rgba(180, 160, 255, 0.15) 100%);
    box-shadow:
        0 0 35px rgba(220, 210, 255, 0.55),
        0 0 100px rgba(160, 130, 255, 0.25);
    opacity: 0.72;
    animation: moonFloat 7s ease-in-out infinite;
}

@keyframes moonFloat {
    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(14px);
    }
}

/* stars */
.star {
    position: absolute;
    width: 4px;
    height: 4px;
    background: #ffffff;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(255,255,255,0.9);
    animation: twinkle 2.5s ease-in-out infinite;
}

@keyframes twinkle {
    0%, 100% {
        opacity: 0.25;
        transform: scale(0.7);
    }
    50% {
        opacity: 1;
        transform: scale(1.4);
    }
}

/* Sakura petals */
.petal {
    position: absolute;
    width: 15px;
    height: 10px;
    background: linear-gradient(135deg, #ffd7ef, #ff8fcb);
    border-radius: 100% 0 100% 0;
    opacity: 0.75;
    filter: drop-shadow(0 0 5px rgba(255, 145, 210, 0.45));
    animation: fall linear infinite;
}

@keyframes fall {
    0% {
        transform: translate3d(0, -12vh, 0) rotate(0deg);
        opacity: 0;
    }

    10% {
        opacity: 0.8;
    }

    50% {
        transform: translate3d(100px, 50vh, 0) rotate(180deg);
    }

    100% {
        transform: translate3d(-120px, 115vh, 0) rotate(360deg);
        opacity: 0;
    }
}

/* different petals */
.p1 { left: 5%;  animation-duration: 12s; animation-delay: -3s; }
.p2 { left: 15%; animation-duration: 15s; animation-delay: -8s; }
.p3 { left: 28%; animation-duration: 11s; animation-delay: -4s; }
.p4 { left: 40%; animation-duration: 17s; animation-delay: -12s; }
.p5 { left: 52%; animation-duration: 13s; animation-delay: -5s; }
.p6 { left: 64%; animation-duration: 16s; animation-delay: -10s; }
.p7 { left: 76%; animation-duration: 12s; animation-delay: -2s; }
.p8 { left: 90%; animation-duration: 18s; animation-delay: -7s; }

/* ---------- CONTENT ---------- */

.block-container {
    position: relative;
    z-index: 2;
}

/* ---------- TOP NAV ---------- */

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0 25px 0;
}

.brand {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.brand span {
    color: #ff9ed8;
}

.brand-small {
    font-size: 0.78rem;
    color: #aaa9c8;
    margin-left: 8px;
}

/* ---------- HERO ---------- */

.hero {
    text-align: center;
    padding: 25px 15px 30px 15px;
}

.hero-badge {
    display: inline-block;
    padding: 7px 15px;
    border-radius: 999px;
    background: rgba(255, 160, 220, 0.10);
    border: 1px solid rgba(255, 180, 230, 0.22);
    color: #ffb6e5;
    font-size: 0.82rem;
    margin-bottom: 18px;
}

.hero h1 {
    font-size: clamp(2.4rem, 6vw, 4.8rem);
    line-height: 1.02;
    margin: 0;
    font-weight: 900;
    letter-spacing: -2px;
    background: linear-gradient(
        100deg,
        #ffffff 15%,
        #ffd1ed 45%,
        #bcb5ff 85%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 650px;
    margin: 18px auto 0 auto;
    color: #b8b6d2;
    font-size: 1.05rem;
    line-height: 1.7;
}

/* ---------- UPLOAD CARD ---------- */

.upload-card {
    max-width: 850px;
    margin: 10px auto 28px auto;
    padding: 34px;
    border-radius: 28px;
    background: rgba(20, 21, 55, 0.68);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow:
        0 25px 80px rgba(0,0,0,0.30),
        inset 0 1px 0 rgba(255,255,255,0.06);
    backdrop-filter: blur(18px);
}

.upload-title {
    text-align: center;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 4px;
}

.upload-subtitle {
    text-align: center;
    color: #9695b5;
    font-size: 0.86rem;
    margin-bottom: 20px;
}

/* ---------- SECTION HEADINGS ---------- */

.section-title {
    font-size: 1.35rem;
    font-weight: 800;
    margin: 30px 0 15px 0;
}

.section-subtitle {
    color: #9897b7;
    margin-top: -8px;
    margin-bottom: 20px;
}

/* ---------- CONTROL CARD ---------- */

.control-card {
    padding: 22px;
    border-radius: 22px;
    background: rgba(20, 21, 55, 0.60);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
}

/* ---------- BUTTONS ---------- */

.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.10);
    background: linear-gradient(135deg, #ff73c6, #a783ff);
    color: white;
    font-weight: 800;
    font-size: 1rem;
    box-shadow: 0 10px 30px rgba(210, 105, 220, 0.25);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 38px rgba(210, 105, 220, 0.38);
    border-color: rgba(255,255,255,0.25);
}

/* ---------- DOWNLOAD BUTTONS ---------- */

.stDownloadButton > button {
    width: 100%;
    min-height: 46px;
    border-radius: 13px;
    background: rgba(255,255,255,0.07);
    color: #f5f3ff;
    border: 1px solid rgba(255,255,255,0.12);
    font-weight: 700;
}

.stDownloadButton > button:hover {
    background: rgba(255,255,255,0.12);
    border-color: rgba(255,170,225,0.35);
}

/* ---------- IMAGE CARDS ---------- */

.image-card {
    padding: 12px;
    border-radius: 22px;
    background: rgba(14, 15, 42, 0.70);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 15px 45px rgba(0,0,0,0.22);
}

.image-label {
    text-align: center;
    font-weight: 750;
    padding: 8px;
    color: #eeeeff;
}

/* ---------- SUCCESS MESSAGE ---------- */

.success-card {
    text-align: center;
    padding: 15px;
    margin: 20px 0;
    border-radius: 16px;
    background: rgba(75, 220, 160, 0.10);
    border: 1px solid rgba(75, 220, 160, 0.22);
    color: #9ef0c9;
}

/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    padding: 45px 0 20px 0;
    color: #777692;
    font-size: 0.8rem;
}

.footer span {
    color: #ff9ed8;
}

/* ---------- MOBILE ---------- */

@media (max-width: 700px) {

    .moon {
        width: 100px;
        height: 100px;
        right: 4%;
        top: 5%;
    }

    .upload-card {
        padding: 20px;
        border-radius: 20px;
    }

    .hero {
        padding-top: 15px;
    }

    .hero h1 {
        letter-spacing: -1px;
    }
}

</style>

<!-- Animated background -->
<div class="anime-bg">

    <div class="moon"></div>

    <div class="star" style="left:8%;top:18%;"></div>
    <div class="star" style="left:18%;top:31%;animation-delay:.7s;"></div>
    <div class="star" style="left:31%;top:13%;animation-delay:1.4s;"></div>
    <div class="star" style="left:46%;top:24%;animation-delay:.3s;"></div>
    <div class="star" style="left:58%;top:12%;animation-delay:1.1s;"></div>
    <div class="star" style="left:70%;top:34%;animation-delay:1.8s;"></div>
    <div class="star" style="left:82%;top:22%;animation-delay:.5s;"></div>
    <div class="star" style="left:94%;top:42%;animation-delay:1.5s;"></div>

    <div class="petal p1"></div>
    <div class="petal p2"></div>
    <div class="petal p3"></div>
    <div class="petal p4"></div>
    <div class="petal p5"></div>
    <div class="petal p6"></div>
    <div class="petal p7"></div>
    <div class="petal p8"></div>

</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown("""
<div class="topbar">
    <div class="brand">
        🌸 Toonify<span>AI</span>
        <span class="brand-small">Image Art Studio</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown("""
<div class="hero">

    <div class="hero-badge">
        ✨ AI-powered image transformation
    </div>

    <h1>Turn your photos<br>into little pieces of art.</h1>

    <p>
        Remove backgrounds and transform your images into
        beautiful cartoon, watercolor, pencil and oil-paint
        styles — all in a few clicks.
    </p>

</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# UPLOAD
# ---------------------------------------------------------

st.markdown("""
<div class="upload-card">

    <div class="upload-title">
        🖼️ Start with an image
    </div>

    <div class="upload-subtitle">
        Upload a JPG or PNG and let the magic begin ✨
    </div>

</div>
""", unsafe_allow_html=True)

my_upload = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

st.markdown("""
<div class="section-title">
    ✨ Customize your creation
</div>

<div class="section-subtitle">
    Choose how you want your artwork to look.
</div>
""", unsafe_allow_html=True)

control_col1, control_col2, control_col3 = st.columns(3)

with control_col1:
    alpha_matting = st.checkbox(
        "✨ Remove background",
        value=True
    )

with control_col2:
    threshold = st.slider(
        "Background threshold",
        0,
        100,
        value=50,
        step=5
    )

with control_col3:
    cartoon_style = st.selectbox(
        "🎨 Art style",
        [
            "Default",
            "Pencil Sketch",
            "Watercolor",
            "Oil Paint"
        ]
    )


# ---------------------------------------------------------
# IMAGE CONVERSION
# ---------------------------------------------------------

def convert_images(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ---------------------------------------------------------
# PROCESSING FUNCTION
# ---------------------------------------------------------

def process_image(uploaded_image, threshold, alpha_matting, cartoon_style):

    if uploaded_image is None:
        st.warning("Please upload an image first.")
        return

    image = Image.open(uploaded_image).convert("RGB")

    # ---------------------------------------------
    # PROCESSING
    # ---------------------------------------------

    with st.spinner("✨ Creating your artwork... this may take a moment."):

        # Background removal
        fixed = remove(
            image,
            alpha_matting=alpha_matting,
            alpha_matting_background_threshold=threshold
        )

        # Convert image to NumPy
        img_cv = np.array(image)

        # Cartoonization
        if cartoon_style == "Default":

            cartoon = cartoonize(img_cv)

        elif cartoon_style == "Pencil Sketch":

            gray, sketch = cv2.pencilSketch(
                img_cv,
                sigma_s=60,
                sigma_r=0.07,
                shade_factor=0.05
            )

            cartoon = sketch

        elif cartoon_style == "Watercolor":

            cartoon = cv2.stylization(
                img_cv,
                sigma_s=60,
                sigma_r=0.6
            )

        elif cartoon_style == "Oil Paint":

            cartoon = cv2.stylization(
                img_cv,
                sigma_s=150,
                sigma_r=0.25
            )

    cartoon_pil = Image.fromarray(cartoon)

    # ---------------------------------------------
    # SUCCESS
    # ---------------------------------------------

    st.markdown("""
    <div class="success-card">
        ✨ Your artwork is ready!
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------
    # RESULTS
    # ---------------------------------------------

    st.markdown("""
    <div class="section-title">
        🖼️ Your results
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="image-card">
            <div class="image-label">
                📸 Original
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.image(
            image,
            use_container_width=True
        )

        st.download_button(
            "⬇️ Download Original",
            data=convert_images(image),
            file_name="original_image.png",
            mime="image/png"
        )

    with col2:

        st.markdown("""
        <div class="image-card">
            <div class="image-label">
                🎨 Cartoonized
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.image(
            cartoon_pil,
            use_container_width=True
        )

        st.download_button(
            "✨ Download Artwork",
            data=convert_images(cartoon_pil),
            file_name="toonify_artwork.png",
            mime="image/png"
        )

    # ---------------------------------------------
    # BACKGROUND REMOVED IMAGE
    # ---------------------------------------------

    st.markdown("""
    <div class="section-title">
        ✨ Background removed
    </div>
    """, unsafe_allow_html=True)

    st.image(
        fixed,
        use_container_width=True
    )

    st.download_button(
        "🌸 Download Background Removed Image",
        data=convert_images(fixed),
        file_name="background_removed.png",
        mime="image/png"
    )


# ---------------------------------------------------------
# RUN ONLY AFTER UPLOAD
# ---------------------------------------------------------

if my_upload:

    process_image(
        my_upload,
        threshold,
        alpha_matting,
        cartoon_style
    )

else:

    st.markdown("""
    <div style="
        text-align:center;
        margin:30px auto;
        padding:25px;
        color:#9695b5;
        max-width:600px;
    ">
        <div style="font-size:2rem;">🌸 ✨ 🌙</div>
        <div style="
            font-size:1rem;
            margin-top:8px;
            color:#aaa9c8;
        ">
            Your canvas is waiting.
            Upload a photo above to begin.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("""
<div class="footer">
    Made with <span>🌸</span> and a little bit of AI magic
    <br>
    Toonify AI · Image Art Studio
</div>
""", unsafe_allow_html=True)
