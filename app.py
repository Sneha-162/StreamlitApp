import streamlit as st
from io import BytesIO
from PIL import Image
from rembg import remove
from huggingface_hub import InferenceClient
import cv2
import numpy as np


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Toonify AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CUSTOM CSS + ANIMATED BACKGROUND
# =========================================================

st.html(
    """
<style>
.stApp {
    background:
        radial-gradient(circle at 15% 15%, rgba(255, 126, 210, 0.18), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(120, 150, 255, 0.20), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(170, 90, 255, 0.16), transparent 35%),
        linear-gradient(135deg, #090b22 0%, #101337 45%, #17102f 100%);
    color: #f7f5ff;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

[data-testid="stAppViewContainer"] {
    position: relative;
    z-index: 1;
}

.anime-bg {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}

.moon {
    position: absolute;
    width: 170px;
    height: 170px;
    right: 7%;
    top: 8%;
    border-radius: 50%;
    background:
        radial-gradient(
            circle at 35% 35%,
            #ffffff 0%,
            #eee8ff 35%,
            #c9c2ff 65%,
            rgba(180, 160, 255, 0.15) 100%
        );
    box-shadow:
        0 0 35px rgba(220, 210, 255, 0.55),
        0 0 100px rgba(160, 130, 255, 0.25);
    opacity: 0.68;
    animation: moonFloat 7s ease-in-out infinite;
}

@keyframes moonFloat {
    0%, 100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(14px);
    }
}

.star {
    position: absolute;
    width: 4px;
    height: 4px;
    background: #ffffff;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.9);
    animation: twinkle 2.5s ease-in-out infinite;
}

@keyframes twinkle {
    0%, 100% {
        opacity: 0.2;
        transform: scale(0.7);
    }

    50% {
        opacity: 1;
        transform: scale(1.4);
    }
}

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

.p1 {
    left: 5%;
    animation-duration: 12s;
    animation-delay: -3s;
}

.p2 {
    left: 15%;
    animation-duration: 15s;
    animation-delay: -8s;
}

.p3 {
    left: 28%;
    animation-duration: 11s;
    animation-delay: -4s;
}

.p4 {
    left: 40%;
    animation-duration: 17s;
    animation-delay: -12s;
}

.p5 {
    left: 52%;
    animation-duration: 13s;
    animation-delay: -5s;
}

.p6 {
    left: 64%;
    animation-duration: 16s;
    animation-delay: -10s;
}

.p7 {
    left: 76%;
    animation-duration: 12s;
    animation-delay: -2s;
}

.p8 {
    left: 90%;
    animation-duration: 18s;
    animation-delay: -7s;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0 20px 0;
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

.hero {
    text-align: center;
    padding: 25px 15px 28px 15px;
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
    max-width: 680px;
    margin: 18px auto 0 auto;
    color: #b8b6d2;
    font-size: 1.05rem;
    line-height: 1.7;
}

.upload-card,
.control-card {
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
    padding: 28px;
    border-radius: 26px;
    background: rgba(20, 21, 55, 0.68);
    border: 1px solid rgba(255, 255, 255, 0.10);
    box-shadow:
        0 25px 80px rgba(0, 0, 0, 0.30),
        inset 0 1px 0 rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(18px);
}

.upload-title {
    text-align: center;
    font-size: 1.2rem;
    font-weight: 750;
}

.upload-subtitle {
    text-align: center;
    color: #9695b5;
    font-size: 0.88rem;
    margin-top: 5px;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 800;
    margin: 30px 0 8px 0;
    color: #f4f2ff;
}

.section-subtitle {
    color: #9897b7;
    margin-bottom: 18px;
}

.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.10);
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
    border-color: rgba(255, 255, 255, 0.25);
}

.stDownloadButton > button {
    width: 100%;
    min-height: 46px;
    border-radius: 13px;
    background: rgba(255, 255, 255, 0.07);
    color: #f5f3ff;
    border: 1px solid rgba(255, 255, 255, 0.12);
    font-weight: 700;
}

.stDownloadButton > button:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 170, 225, 0.35);
}

[data-testid="stFileUploader"] {
    max-width: 900px;
    margin: 0 auto;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(14, 15, 42, 0.62);
    border: 1.5px dashed rgba(255, 174, 224, 0.38);
    border-radius: 22px;
    padding: 18px;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(255, 174, 224, 0.75);
    background: rgba(30, 26, 67, 0.72);
}

.image-card {
    padding: 12px;
    border-radius: 22px;
    background: rgba(14, 15, 42, 0.70);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 15px 45px rgba(0, 0, 0, 0.22);
}

.image-label {
    text-align: center;
    font-weight: 750;
    padding: 8px;
    color: #eeeeff;
}

.success-card {
    text-align: center;
    padding: 15px;
    margin: 20px 0;
    border-radius: 16px;
    background: rgba(75, 220, 160, 0.10);
    border: 1px solid rgba(75, 220, 160, 0.22);
    color: #9ef0c9;
}

.empty-state {
    text-align: center;
    margin: 30px auto;
    padding: 25px;
    color: #9695b5;
}

.empty-icons {
    font-size: 2rem;
    letter-spacing: 8px;
}

.empty-text {
    margin-top: 10px;
    color: #aaa9c8;
}

.footer {
    text-align: center;
    padding: 45px 0 20px 0;
    color: #777692;
    font-size: 0.8rem;
}

.footer span {
    color: #ff9ed8;
}

@media (max-width: 700px) {
    .moon {
        width: 100px;
        height: 100px;
        right: 4%;
        top: 5%;
    }

    .hero {
        padding-top: 12px;
    }

    .hero h1 {
        letter-spacing: -1px;
    }

    .upload-card,
    .control-card {
        padding: 20px;
        border-radius: 20px;
    }
}
</style>

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
"""
)


# =========================================================
# HEADER
# =========================================================

st.html(
    """
<div class="topbar">
    <div class="brand">
        🌸 Toonify<span>AI</span>
        <span class="brand-small">Image Art Studio</span>
    </div>
</div>
"""
)


# =========================================================
# HERO
# =========================================================

st.html(
    """
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
"""
)


# =========================================================
# UPLOAD CARD
# =========================================================

st.html(
    """
<div class="upload-card">
    <div class="upload-title">
        🖼️ Start with an image
    </div>

    <div class="upload-subtitle">
        Upload a JPG or PNG and let the magic begin ✨
    </div>
</div>
"""
)

uploaded_image = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)


# =========================================================
# CUSTOMIZATION
# =========================================================

st.html(
    """
<div class="section-title">
    ✨ Customize your creation
</div>

<div class="section-subtitle">
    Choose how you want your artwork to look.
</div>
"""
)

control_col1, control_col2, control_col3 = st.columns(3)

with control_col1:
    alpha_matting = st.checkbox(
        "✨ Remove background",
        value=True,
    )

with control_col2:
    threshold = st.slider(
        "Background threshold",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
    )

with control_col3:
    cartoon_style = st.selectbox(
        "🎨 AI Art style",
        [
            "Anime Cartoon",
            "Watercolor",
            "Manga",
            "Digital Art",
            "Classic Cartoon",
        ],
    )


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def convert_image_to_bytes(image):
    """Convert a PIL image to PNG bytes."""
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


# =========================================================
# HUGGING FACE AI ART GENERATION
# =========================================================

STYLE_PROMPTS = {
    "Anime Cartoon": """
Transform this photograph into a polished anime-inspired
cartoon illustration.

Preserve the person's identity, facial features, pose,
clothing, proportions and overall composition.

Use clean expressive outlines, soft vibrant colors,
subtle shading and a professional digital-art finish.

Do not add extra people or objects.
Do not change the person's identity.
""",

    "Watercolor": """
Transform this photograph into a beautiful watercolor
illustration.

Preserve the person's identity, facial features, pose,
clothing, proportions and overall composition.

Use soft watercolor pigments, delicate brush textures,
natural colors and elegant painted edges.

Do not add extra people or objects.
""",

    "Manga": """
Transform this photograph into a polished manga-style
illustration.

Preserve the person's identity, facial features, pose,
clothing, proportions and overall composition.

Use clean expressive ink lines, manga-style shading,
detailed illustrated features and controlled highlights.

Do not add extra people or objects.
""",

    "Digital Art": """
Transform this photograph into polished professional
digital artwork.

Preserve the person's identity, facial features, pose,
clothing, proportions and overall composition.

Use clean refined edges, beautiful colors, subtle
cinematic lighting and high-quality digital illustration.

Do not add extra people or objects.
""",

    "Classic Cartoon": """
Transform this photograph into a colorful cartoon
illustration.

Preserve the person's identity, facial features, pose,
clothing, proportions and overall composition.

Use bold clean outlines, smooth colors, playful shading
and a friendly animated finish.

Do not add extra people or objects.
"""
}


def generate_ai_art(image, selected_style):
    """
    Send the image to Hugging Face and generate the
    selected artistic style using FLUX.2-klein-9B.
    """

    client = InferenceClient(
        provider="auto",
        api_key=st.secrets["HF_TOKEN"]
    )

    result = client.image_to_image(
        image=image,
        prompt=STYLE_PROMPTS[selected_style],
        model="black-forest-labs/FLUX.2-klein-9B"
    )

    return result


# =========================================================
# IMAGE PROCESSING
# =========================================================

def process_image(
    uploaded_file,
    background_threshold,
    remove_background,
    selected_style,
):
    """Process and display the uploaded image."""

    original_image = Image.open(uploaded_file).convert("RGB")

    with st.spinner("✨ Creating your artwork... this may take a moment."):
        # Background removal
        background_removed = original_image.copy()

        # Resize very large phone images before sending them
        # to the AI API. This reduces upload size and memory usage.
        ai_image = original_image.copy()
        ai_image.thumbnail(
            (1600, 1600),
            Image.Resampling.LANCZOS,
        )

        # Generate artwork using Hugging Face
        artwork_image = generate_ai_art(
            ai_image,
            selected_style,
        )

    # =====================================================
    # SUCCESS MESSAGE
    # =====================================================

    st.html(
        """
<div class="success-card">
    ✨ Your artwork is ready!
</div>
"""
    )

    # =====================================================
    # RESULTS
    # =====================================================

    st.html(
        """
<div class="section-title">
    🖼️ Your results
</div>
"""
    )

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.html(
            """
<div class="image-card">
    <div class="image-label">
        📸 Original
    </div>
</div>
"""
        )

        st.image(
            original_image,
            use_container_width=True,
        )

        st.download_button(
            label="⬇️ Download Original",
            data=convert_image_to_bytes(original_image),
            file_name="original_image.png",
            mime="image/png",
        )

    with result_col2:
        st.html(
            """
<div class="image-card">
    <div class="image-label">
        🎨 Cartoonized
    </div>
</div>
"""
        )

        st.image(
            artwork_image,
            use_container_width=True,
        )

        st.download_button(
            label="✨ Download Artwork",
            data=convert_image_to_bytes(artwork_image),
            file_name="toonify_artwork.png",
            mime="image/png",
        )

    # =====================================================
    # BACKGROUND-REMOVED RESULT
    # =====================================================

    st.html(
        """
<div class="section-title">
    ✨ Background removed
</div>
"""
    )

    st.image(
        background_removed,
        use_container_width=True,
    )

    st.download_button(
        label="🌸 Download Background Removed Image",
        data=convert_image_to_bytes(background_removed),
        file_name="background_removed.png",
        mime="image/png",
    )


# =========================================================
# RUN APP
# =========================================================

if uploaded_image is not None:
    process_image(
        uploaded_file=uploaded_image,
        background_threshold=threshold,
        remove_background=alpha_matting,
        selected_style=cartoon_style,
    )
else:
    st.html(
        """
<div class="empty-state">
    <div class="empty-icons">
        🌸 ✨ 🌙
    </div>

    <div class="empty-text">
        Your canvas is waiting.
        Upload a photo above to begin.
    </div>
</div>
"""
    )


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
<div class="footer">
    Made with <span>🌸</span> and a little bit of AI magic
    <br>
    Toonify AI · Image Art Studio
</div>
"""
)
