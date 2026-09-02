import streamlit as st
from io import BytesIO
from PIL import Image
import base64
import html
import streamlit.components.v1 as components


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
        radial-gradient(circle at 15% 15%, rgba(255,126,210,.18), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(120,150,255,.20), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(170,90,255,.16), transparent 35%),
        linear-gradient(135deg,#090b22 0%,#101337 45%,#17102f 100%);
    color:#f7f5ff;
}

#MainMenu, header, footer { visibility:hidden; }

[data-testid="stAppViewContainer"] {
    position:relative;
    z-index:1;
}

.anime-bg {
    position:fixed;
    inset:0;
    overflow:hidden;
    pointer-events:none;
    z-index:0;
}

.moon {
    position:absolute;
    width:170px;
    height:170px;
    right:7%;
    top:8%;
    border-radius:50%;
    background:
        radial-gradient(circle at 35% 35%,
            #ffffff 0%, #eee8ff 35%, #c9c2ff 65%,
            rgba(180,160,255,.15) 100%);
    box-shadow:
        0 0 35px rgba(220,210,255,.55),
        0 0 100px rgba(160,130,255,.25);
    opacity:.68;
    animation:moonFloat 7s ease-in-out infinite;
}

@keyframes moonFloat {
    0%,100% { transform:translateY(0); }
    50% { transform:translateY(14px); }
}

.star {
    position:absolute;
    width:4px;
    height:4px;
    background:#fff;
    border-radius:50%;
    box-shadow:0 0 10px rgba(255,255,255,.9);
    animation:twinkle 2.5s ease-in-out infinite;
}

@keyframes twinkle {
    0%,100% { opacity:.2; transform:scale(.7); }
    50% { opacity:1; transform:scale(1.4); }
}

.petal {
    position:absolute;
    width:15px;
    height:10px;
    background:linear-gradient(135deg,#ffd7ef,#ff8fcb);
    border-radius:100% 0 100% 0;
    opacity:.75;
    filter:drop-shadow(0 0 5px rgba(255,145,210,.45));
    animation:fall linear infinite;
}

@keyframes fall {
    0% {
        transform:translate3d(0,-12vh,0) rotate(0deg);
        opacity:0;
    }
    10% { opacity:.8; }
    50% {
        transform:translate3d(100px,50vh,0) rotate(180deg);
    }
    100% {
        transform:translate3d(-120px,115vh,0) rotate(360deg);
        opacity:0;
    }
}

.p1 { left:5%; animation-duration:12s; animation-delay:-3s; }
.p2 { left:15%; animation-duration:15s; animation-delay:-8s; }
.p3 { left:28%; animation-duration:11s; animation-delay:-4s; }
.p4 { left:40%; animation-duration:17s; animation-delay:-12s; }
.p5 { left:52%; animation-duration:13s; animation-delay:-5s; }
.p6 { left:64%; animation-duration:16s; animation-delay:-10s; }
.p7 { left:76%; animation-duration:12s; animation-delay:-2s; }
.p8 { left:90%; animation-duration:18s; animation-delay:-7s; }

.topbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:8px 0 20px;
}

.brand {
    font-size:1.55rem;
    font-weight:800;
    letter-spacing:-.5px;
}

.brand span { color:#ff9ed8; }

.brand-small {
    font-size:.78rem;
    color:#aaa9c8;
    margin-left:8px;
}

.hero {
    text-align:center;
    padding:25px 15px 28px;
}

.hero-badge {
    display:inline-block;
    padding:7px 15px;
    border-radius:999px;
    background:rgba(255,160,220,.10);
    border:1px solid rgba(255,180,230,.22);
    color:#ffb6e5;
    font-size:.82rem;
    margin-bottom:18px;
}

.hero h1 {
    font-size:clamp(2.4rem,6vw,4.8rem);
    line-height:1.02;
    margin:0;
    font-weight:900;
    letter-spacing:-2px;
    background:linear-gradient(100deg,#fff 15%,#ffd1ed 45%,#bcb5ff 85%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero p {
    max-width:680px;
    margin:18px auto 0;
    color:#b8b6d2;
    font-size:1.05rem;
    line-height:1.7;
}

.upload-card {
    max-width:900px;
    margin:auto;
    padding:28px;
    border-radius:26px;
    background:rgba(20,21,55,.68);
    border:1px solid rgba(255,255,255,.10);
    box-shadow:
        0 25px 80px rgba(0,0,0,.30),
        inset 0 1px 0 rgba(255,255,255,.06);
    backdrop-filter:blur(18px);
}

.upload-title {
    text-align:center;
    font-size:1.2rem;
    font-weight:750;
}

.upload-subtitle {
    text-align:center;
    color:#9695b5;
    font-size:.88rem;
    margin-top:5px;
}

.section-title {
    font-size:1.35rem;
    font-weight:800;
    margin:30px 0 8px;
    color:#f4f2ff;
}

.section-subtitle {
    color:#9897b7;
    margin-bottom:18px;
}

[data-testid="stFileUploader"] {
    max-width:900px;
    margin:0 auto;
}

[data-testid="stFileUploaderDropzone"] {
    background:rgba(14,15,42,.62);
    border:1.5px dashed rgba(255,174,224,.38);
    border-radius:22px;
    padding:18px;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color:rgba(255,174,224,.75);
    background:rgba(30,26,67,.72);
}

.stButton > button {
    width:100%;
    min-height:48px;
    border-radius:14px;
    border:1px solid rgba(255,255,255,.10);
    background:linear-gradient(135deg,#ff73c6,#a783ff);
    color:white;
    font-weight:800;
    font-size:1rem;
    box-shadow:0 10px 30px rgba(210,105,220,.25);
    transition:all .2s ease;
}

.stButton > button:hover {
    transform:translateY(-2px);
    box-shadow:0 14px 38px rgba(210,105,220,.38);
}

.empty-state {
    text-align:center;
    margin:30px auto;
    padding:25px;
    color:#9695b5;
}

.empty-icons {
    font-size:2rem;
    letter-spacing:8px;
}

.empty-text {
    margin-top:10px;
    color:#aaa9c8;
}

.success-card {
    text-align:center;
    padding:15px;
    margin:20px 0;
    border-radius:16px;
    background:rgba(75,220,160,.10);
    border:1px solid rgba(75,220,160,.22);
    color:#9ef0c9;
}

.footer {
    text-align:center;
    padding:45px 0 20px;
    color:#777692;
    font-size:.8rem;
}

.footer span { color:#ff9ed8; }

@media (max-width:700px) {
    .moon {
        width:100px;
        height:100px;
        right:4%;
        top:5%;
    }

    .hero { padding-top:12px; }
    .hero h1 { letter-spacing:-1px; }

    .upload-card {
        padding:20px;
        border-radius:20px;
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

    <h1>
        Turn your photos<br>
        into little pieces of art.
    </h1>

    <p>
        Transform your photos into beautiful anime, watercolor,
        manga, digital-art and classic-cartoon styles —
        right in your browser.
    </p>
</div>
"""
)


# =========================================================
# UPLOAD
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

control_col1, control_col2 = st.columns(2)

with control_col1:
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

with control_col2:
    output_quality = st.selectbox(
        "⚡ Generation quality",
        ["Fast", "High quality"],
        index=0,
    )


# =========================================================
# STYLE PROMPTS
# =========================================================

STYLE_PROMPTS = {
    "Anime Cartoon": """
Transform the supplied photograph into a polished anime-inspired
cartoon illustration.

Preserve the person's identity, facial features, pose, clothing,
proportions and overall composition as closely as possible.

Use clean expressive outlines, soft vibrant colors, subtle shading,
beautiful anime-inspired eyes and a professional digital-art finish.

Do not add extra people or objects.
Do not change the person's identity.
Keep the original scene recognizable.
""",

    "Watercolor": """
Transform the supplied photograph into a beautiful hand-painted
watercolor illustration.

Preserve the person's identity, facial features, pose, clothing,
proportions and overall composition.

Use soft watercolor pigments, delicate brush textures, natural colors,
elegant painted edges and subtle paper-like texture.

Do not add extra people or objects.
Keep the original scene recognizable.
""",

    "Manga": """
Transform the supplied photograph into a polished manga-style
illustration.

Preserve the person's identity, facial features, pose, clothing,
proportions and overall composition.

Use clean expressive ink lines, manga-style shading,
detailed illustrated features and controlled highlights.

Do not add extra people or objects.
""",

    "Digital Art": """
Transform the supplied photograph into polished professional
digital artwork.

Preserve the person's identity, facial features, pose, clothing,
proportions and overall composition.

Use clean refined edges, beautiful colors, subtle cinematic lighting,
smooth digital painting and a premium illustration finish.

Do not add extra people or objects.
""",

    "Classic Cartoon": """
Transform the supplied photograph into a colorful polished
cartoon illustration.

Preserve the person's identity, facial features, pose, clothing,
proportions and overall composition.

Use bold clean outlines, smooth colors, playful shading,
simplified but recognizable forms and a friendly animated finish.

Do not add extra people or objects.
"""
}


# =========================================================
# IMAGE → DATA URI
# =========================================================

def image_to_data_uri(image):
    image = image.convert("RGB").copy()

    image.thumbnail(
        (1536, 1536),
        Image.Resampling.LANCZOS
    )

    buffer = BytesIO()

    image.save(
        buffer,
        format="JPEG",
        quality=90,
        optimize=True
    )

    encoded = base64.b64encode(
        buffer.getvalue()
    ).decode("ascii")

    return "data:image/jpeg;base64," + encoded


# =========================================================
# PUTER.JS EDITOR
# =========================================================

def render_puter_editor(image_data_uri, selected_style, quality):

    prompt = STYLE_PROMPTS[selected_style].strip()
    model = "black-forest-labs/flux-2-klein-4b"
    megapixels = "0.5" if quality == "Fast" else "1"

    # Escape values before inserting them into JavaScript.
    safe_prompt = (
        prompt
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )

    safe_image = (
        image_data_uri
        .replace("\\", "\\\\")
        .replace('"', '\\"')
    )

    safe_style = html.escape(selected_style)

    # IMPORTANT:
    # This is a normal raw Python string, NOT an f-string.
    # Therefore JavaScript { } are completely safe.
    component_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://js.puter.com/v2/"></script>

<style>
* { box-sizing:border-box; }

body {
    margin:0;
    padding:4px;
    font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
    background:transparent;
    color:#f7f5ff;
}

.panel {
    padding:18px;
    border-radius:22px;
    background:rgba(20,21,55,.72);
    border:1px solid rgba(255,255,255,.10);
    box-shadow:0 20px 55px rgba(0,0,0,.24);
}

.top {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:12px;
    margin-bottom:16px;
}

.title {
    font-size:1.05rem;
    font-weight:800;
}

.badge {
    padding:6px 10px;
    border-radius:999px;
    background:rgba(255,159,216,.10);
    border:1px solid rgba(255,180,230,.18);
    color:#ffb6e5;
    font-size:.75rem;
    white-space:nowrap;
}

.images {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:14px;
}

.card {
    background:rgba(9,11,34,.68);
    border:1px solid rgba(255,255,255,.08);
    border-radius:18px;
    padding:10px;
    overflow:hidden;
}

.label {
    text-align:center;
    font-size:.82rem;
    font-weight:750;
    padding:7px;
}

.preview {
    width:100%;
    max-height:520px;
    object-fit:contain;
    display:block;
    border-radius:13px;
    background:rgba(255,255,255,.03);
}

.result-empty {
    min-height:280px;
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    color:#9290ad;
    padding:20px;
}

.controls {
    margin-top:15px;
    display:flex;
    gap:10px;
    flex-wrap:wrap;
}

button,
.download {
    border:0;
    border-radius:13px;
    min-height:46px;
    padding:0 18px;
    font-weight:800;
    cursor:pointer;
    text-decoration:none;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    font-size:.92rem;
}

#generate {
    flex:1;
    color:white;
    background:linear-gradient(135deg,#ff73c6,#a783ff);
    box-shadow:0 10px 25px rgba(210,105,220,.25);
}

#fallback {
    color:#eeeaff;
    background:rgba(255,255,255,.07);
    border:1px solid rgba(255,255,255,.10);
}

.download {
    width:100%;
    margin-top:10px;
    color:#f5f3ff;
    background:rgba(255,255,255,.07);
    border:1px solid rgba(255,255,255,.12);
}

button:disabled {
    opacity:.55;
    cursor:wait;
}

.status {
    margin-top:12px;
    padding:11px 13px;
    border-radius:12px;
    background:rgba(255,255,255,.045);
    color:#aaa8c5;
    font-size:.82rem;
    line-height:1.5;
    text-align:center;
}

.success {
    color:#9ef0c9;
    background:rgba(75,220,160,.08);
    border:1px solid rgba(75,220,160,.16);
}

.warning {
    color:#ffd58f;
    background:rgba(255,190,80,.08);
    border:1px solid rgba(255,190,80,.16);
}

@media(max-width:700px) {
    .images { grid-template-columns:1fr; }

    .top {
        align-items:flex-start;
        flex-direction:column;
    }

    .result-empty { min-height:180px; }

    .controls { flex-direction:column; }

    button { width:100%; }
}
</style>
</head>

<body>

<div class="panel">

    <div class="top">
        <div class="title">🎨 __STYLE__</div>

        <div class="badge">
            Puter.js · FLUX.2 Klein
        </div>
    </div>

    <div class="images">

        <div class="card">
            <div class="label">📸 Original</div>

            <img
                id="original"
                class="preview"
                src="__IMAGE__"
                alt="Original image">
        </div>

        <div class="card">
            <div class="label">✨ AI Artwork</div>

            <div id="resultBox" class="result-empty">
                Your transformed image will appear here.
            </div>
        </div>

    </div>

    <div class="controls">

        <button id="generate" onclick="generateArtwork()">
            ✨ Generate AI Artwork
        </button>

        <button id="fallback" onclick="makeFallback()">
            🎨 Quick Cartoon
        </button>

    </div>

    <div id="status" class="status">
        AI generation runs through Puter.js.
        You may be asked to sign in to Puter the first time.
    </div>

    <a
        id="download"
        class="download"
        style="display:none"
        download="toonify_artwork.png">
        ⬇️ Download Artwork
    </a>

</div>


<script>

const SOURCE_IMAGE = "__IMAGE__";
const STYLE_PROMPT = `__PROMPT__`;
const MODEL = "__MODEL__";
const MEGAPIXELS = "__MEGAPIXELS__";


function setStatus(message, type = "") {

    const element = document.getElementById("status");

    element.textContent = message;
    element.className = "status " + type;
}


function showResult(source, fallback = false) {

    const box = document.getElementById("resultBox");

    box.className = "";
    box.style.padding = "0";

    const image = document.createElement("img");

    image.className = "preview";
    image.src = source;
    image.alt = "Generated artwork";

    box.innerHTML = "";
    box.appendChild(image);


    const download = document.getElementById("download");

    download.href = source;
    download.style.display = "flex";


    if (fallback) {

        setStatus(
            "Quick Cartoon is ready.",
            "warning"
        );

    } else {

        setStatus(
            "✨ Your AI artwork is ready!",
            "success"
        );

    }
}


async function generateArtwork() {

    const button = document.getElementById("generate");

    button.disabled = true;
    button.textContent = "✨ Creating artwork...";

    setStatus(
        "Connecting to Puter and generating your artwork. Please wait..."
    );


    try {

        const result = await puter.ai.txt2img(
            STYLE_PROMPT,
            {
                model: MODEL,
                input_images: [
                    SOURCE_IMAGE
                ],
                output_megapixels: MEGAPIXELS
            }
        );


        if (!result || !result.src) {

            throw new Error(
                "Puter did not return an image."
            );
        }


        showResult(result.src, false);

    }

    catch(error) {

        console.error(error);

        setStatus(
            "AI generation could not be completed. You can use Quick Cartoon below.",
            "warning"
        );

    }

    finally {

        button.disabled = false;
        button.textContent = "✨ Generate AI Artwork";

    }
}


function makeFallback() {

    const image = new Image();


    image.onload = function() {

        const maxSize = 1100;

        const scale = Math.min(
            1,
            maxSize / Math.max(
                image.width,
                image.height
            )
        );


        const canvas = document.createElement("canvas");

        canvas.width = Math.max(
            1,
            Math.round(image.width * scale)
        );

        canvas.height = Math.max(
            1,
            Math.round(image.height * scale)
        );


        const context = canvas.getContext(
            "2d",
            {
                willReadFrequently: true
            }
        );


        context.drawImage(
            image,
            0,
            0,
            canvas.width,
            canvas.height
        );


        const imageData = context.getImageData(
            0,
            0,
            canvas.width,
            canvas.height
        );


        const data = imageData.data;


        for (
            let i = 0;
            i < data.length;
            i += 4
        ) {

            let r = data[i];
            let g = data[i + 1];
            let b = data[i + 2];

            const average = (r + g + b) / 3;

            r = r + (r - average) * 0.18;
            g = g + (g - average) * 0.18;
            b = b + (b - average) * 0.18;

            r = Math.round(r / 32) * 32;
            g = Math.round(g / 32) * 32;
            b = Math.round(b / 32) * 32;

            data[i] =
                Math.max(0, Math.min(255, r));

            data[i + 1] =
                Math.max(0, Math.min(255, g));

            data[i + 2] =
                Math.max(0, Math.min(255, b));
        }


        context.putImageData(
            imageData,
            0,
            0
        );


        const source = canvas.toDataURL("image/png");

        showResult(source, true);

    };


    image.src = SOURCE_IMAGE;
}

</script>

</body>
</html>
"""

    component_html = (
        component_html
        .replace("__IMAGE__", safe_image)
        .replace("__PROMPT__", safe_prompt)
        .replace("__MODEL__", model)
        .replace("__MEGAPIXELS__", megapixels)
        .replace("__STYLE__", safe_style)
    )

    components.html(
        component_html,
        height=820,
        scrolling=False
    )


# =========================================================
# RUN APP
# =========================================================

if uploaded_image is not None:

    original_image = (
        Image.open(uploaded_image)
        .convert("RGB")
    )

    image_data_uri = image_to_data_uri(
        original_image
    )

    st.html(
        """
<div class="success-card">
    ✨ Image uploaded successfully —
    choose a style and generate your artwork below.
</div>
"""
    )

    render_puter_editor(
        image_data_uri=image_data_uri,
        selected_style=cartoon_style,
        quality=output_quality
    )

    st.caption(
        "💡 Fast mode is recommended for a public demo. "
        "If AI generation is unavailable, Quick Cartoon "
        "works locally in the browser."
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
