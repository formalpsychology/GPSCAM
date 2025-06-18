# 📷 GPS Camera with Full Address and Weather Overlay

Capture professional-quality images with embedded GPS coordinates, full street-level address, real-time weather, and a simulated satellite-style map overlay — all from your browser.

---

## 🌟 Features

- 📍 Automatic GPS location detection via IP
- 🏠 Reverse geocoding with full street address
- 🌤️ Weather info (temperature, condition, humidity, wind)
- 🗺️ Satellite-style terrain map with location pin
- 🖼️ 9:16 optimized professional image overlay
- 📥 One-click download in high-quality JPEG
- ✅ Fully mobile-compatible (runs in browser)
- 🎨 Stylish and modern UI (Streamlit + CSS)

---

## 🚀 Try It Online

👉 [Launch the app on Streamlit Cloud](https://gpscam.streamlit.app)  
*(requires camera and location permission in browser)*

---

## 📦 Installation

```bash
git clone https://github.com/formalpsychology/gps-camera.git
cd gps-camera
pip install -r requirements.txt
Then run it locally:

bash
Copy
Edit
streamlit run app.py
🔧 Configuration
Sign up at OpenWeatherMap for a free API key.

Replace the default key in the script:

python
Copy
Edit
self.api_key = "YOUR_OPENWEATHER_API_KEY"
📁 Files Included
app.py – Main Streamlit app

requirements.txt – Required Python packages

runtime.txt (optional) – Python version for deployment

README.md – Project description and instructions

📷 Screenshots
Original Photo	GPS + Address Overlay

(Add actual screenshots in a screenshots/ folder)

🛡️ License
MIT License – use, modify, and share freely.

🙋‍♂️ Author
Roshan Kumar
GitHub Profile

Built with ❤️ using Streamlit, OpenStreetMap, and OpenWeatherMap
