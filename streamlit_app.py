import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
import io
import base64
import os

# Try to load a nice font
try:
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if not os.path.exists(font_path):
        font_path = "DejaVuSans.ttf"
    font = ImageFont.truetype(font_path, 20)
except:
    font = ImageFont.load_default()

# Streamlit page setup
st.set_page_config(page_title="Polaroid Strip Generator", page_icon="🎞️", layout="centered")

# CSS for butter yellow background
st.markdown("""
    <style>
        body {
            background-color: #fff8dc;
        }
        .stApp {
            background-color: #fff8dc;
            padding: 2rem;
        }
        .title {
            font-family: 'Georgia', serif;
            text-align: center;
            color: #4a3f35;
            font-size: 2.5rem;
        }
        .subtitle {
            font-family: 'Courier New', monospace;
            color: #6e5d44;
            text-align: center;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        img {
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
        }
        a {
            text-decoration: none;
            font-size: 1.1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">Polaroid Strip Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Take 4 black & white photos. Timeless memories await </div>', unsafe_allow_html=True)

# Sticker messages
sticker_texts = [
    "Pause. Smile. Remember.",
    "Unfiltered Joy ",
    "This is a core memory",
    "You look like art today ",
    "Made you smile!",
    "Caught in a candid",
    "Snapshot of joy",
    "Moments like these "
]

# Take 4 black & white photos
photos = []
for i in range(1, 5):
    img = st.camera_input(f"Take Photo {i}")
    if img:
        image = Image.open(img).convert("RGB").resize((400, 500))
        bw_image = ImageOps.grayscale(image).convert("RGB")
        photos.append(bw_image)

# Generate strip when ready
if len(photos) == 4 and st.button("🖤 Generate My Polaroid Strip"):
    block_height = 550
    strip_height = 4 * block_height + 80
    strip = Image.new("RGB", (400, strip_height), (255, 249, 196))  # butter yellow tone
    draw = ImageDraw.Draw(strip)

    for idx, photo in enumerate(photos):
        y_offset = idx * block_height
        strip.paste(photo, (0, y_offset))

        # Draw sticker text
        sticker = random.choice(sticker_texts)
        bbox = draw.textbbox((0, 0), sticker, font=font)
        text_w = bbox[2] - bbox[0]
        draw.text(((400 - text_w) // 2, y_offset + 510), sticker, fill=(70, 70, 70), font=font)

    # Footer text
    footer = "Captured with love in this moment."
    bbox_footer = draw.textbbox((0, 0), footer, font=font)
    fw = bbox_footer[2] - bbox_footer[0]
    draw.text(((400 - fw) // 2, strip_height - 60), footer, fill=(50, 40, 30), font=font)

    # Show the strip
    st.image(strip, caption="Your Black & White Polaroid Strip", use_container_width=False)

    # Download link
    buffered = io.BytesIO()
    strip.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()
    b64 = base64.b64encode(img_bytes).decode()
    href = f'<a href="data:image/jpeg;base64,{b64}" download="polaroid_strip_bw.jpg">📥 Download your polaroid strip</a>'
    st.markdown(href, unsafe_allow_html=True)
