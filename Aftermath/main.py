import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from datetime import datetime
import os
import platform
import json
import base64

OPENWEATHER_API_KEY = "381f280420c0f91c6362d94c50f427e3"

if platform.system() == "Windows":
    FONT_PATH = "C:/Windows/Fonts/arial.ttf"
else:
    FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def get_address(lat, lon):
    try:
        res = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json"},
            headers={"User-Agent": "GeoCameraApp/1.0"}
        )
        return res.json().get("display_name", "Unknown location")
    except:
        return "Unknown location"

def get_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        temp = data["main"]["temp"]
        condition = data["weather"][0]["main"]
        return f"{condition}, {int(temp)}°C"
    except:
        return "Weather unavailable"

def get_static_map(lat, lon, width=300, height=200):
    map_url = f"https://static-maps.yandex.ru/1.x/?ll={lon},{lat}&z=17&l=sat&size={width},{height}&pt={lon},{lat},pm2rdm"
    response = requests.get(map_url)
    return Image.open(BytesIO(response.content))

def create_overlay_image(frame, address, lat, lon, weather, timestamp):
    base_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    overlay_height = 160
    map_img = get_static_map(lat, lon, width=160, height=160)

    overlay = Image.new("RGB", (base_image.width, overlay_height), (30, 30, 30))
    draw = ImageDraw.Draw(overlay)
    font_big = ImageFont.truetype(FONT_PATH, 22)
    font_small = ImageFont.truetype(FONT_PATH, 16)

    overlay.paste(map_img.resize((120, 120)), (10, 20))
    draw.text((140, 10), address, font=font_big, fill=(255, 255, 255))
    draw.text((140, 50), f"Lat: {lat:.6f}, Lon: {lon:.6f}", font=font_small, fill=(200, 200, 200))
    draw.text((140, 70), f"Weather: {weather}", font=font_small, fill=(200, 200, 200))
    draw.text((140, 90), f"Time: {timestamp}", font=font_small, fill=(100, 200, 255))

    final_image = Image.new("RGB", (base_image.width, base_image.height + overlay_height))
    final_image.paste(base_image, (0, 0))
    final_image.paste(overlay, (0, base_image.height))
    return final_image

st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    .stButton>button {font-size: 1.5em; padding: 0.75em 2em; background-color: #0099ff; color: white; border-radius: 10px;}
    </style>
    """, unsafe_allow_html=True)

st.title("📷 Geo-Tagged Camera App")

# Inject JavaScript to get GPS coordinates
components.html("""
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const coords = {
                lat: position.coords.latitude,
                lon: position.coords.longitude
            };
            const input = window.parent.document.querySelector('[data-testid="stTextArea"] textarea');
            if (input) {
                input.value = JSON.stringify(coords);
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }
        },
        (err) => {
            alert("Location access denied or unavailable.");
        },
        { enableHighAccuracy: true }
    );
    </script>
""", height=0)

coords_input = st.text_area("📍", height=68, label_visibility="collapsed")

lat, lon = None, None
if coords_input:
    try:
        coords = json.loads(coords_input)
        lat, lon = coords["lat"], coords["lon"]
    except:
        st.warning("Waiting for valid GPS coordinates...")

image_file = st.camera_input("📸 Capture Photo")

if image_file and lat and lon:
    try:
        address = get_address(lat, lon)
        weather = get_weather(lat, lon)
        timestamp = datetime.now().strftime("%a, %d %b %Y %H:%M")

        frame = Image.open(image_file)
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        result_img = create_overlay_image(frame, address, lat, lon, weather, timestamp)

        st.markdown(f"**📍 {address}**")
        st.image(result_img, caption="📷 Captured Image with Geo Data", use_container_width=True)

        buf = BytesIO()
        result_img.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        st.download_button("💾 Save Image", data=byte_im, file_name="geo_photo.jpg", mime="image/jpeg")

        # Mobile fallback link
        b64_img = base64.b64encode(byte_im).decode()
        href = f'<a href="data:image/jpeg;base64,{b64_img}" download="geo_photo.jpg">📥 Tap here if the button above does not work</a>'
        st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Failed to render image: {e}")
