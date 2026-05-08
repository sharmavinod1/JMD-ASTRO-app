import streamlit as st
import swisseph as swe
from datetime import datetime

# ऐप का नाम और लेआउट
st.set_page_config(page_title="Vinod Astro Pro", layout="wide")
st.markdown("<h1 style='text-align: center; color: #d35400;'>Vinod Astrology Software (Lahiri)</h1>", unsafe_allow_html=True)

# --- इनपुट विभाग ---
with st.sidebar:
    st.header("जातक का विवरण")
    name = st.text_input("जातक का नाम", value="विनोद")
    
    dob = st.date_input("जन्म तिथि", value=datetime(1979, 5, 27), 
                        min_value=datetime(1900, 1, 1), max_value=datetime(2100, 12, 31))
    
    time_str = st.text_input("जन्म समय (HH:MM जैसे 02:50)", value="02:50")
    try:
        tob = datetime.strptime(time_str, "%H:%M").time()
    except:
        st.error("समय सही लिखें")
        tob = datetime.strptime("00:00", "%H:%M").time()

    st.subheader("जन्म स्थान")
    city = st.text_input("शहर", value="Solapur")
    lat = st.number_input("अक्षांश (Latitude)", value=17.6599, format="%.4f")
    lon = st.number_input("रेखांश (Longitude)", value=75.9064, format="%.4f")

# --- गणना के फंक्शन ---
def format_deg(decimal_deg):
    d = int(decimal_deg % 30)
    total_seconds = decimal_deg * 3600
    m = int((total_seconds // 60) % 60)
    s = int(total_seconds % 60)
    return f"{d}° {m}' {s}\""

def draw_kundli(asc_sign, house_planets):
    svg = f'<svg width="350" height="350" viewBox="0 0 300 300" style="display:block; margin:auto; background:#fff; border:2px solid #d35400;">'
    svg += '<line x1="0" y1="0" x2="300" y2="300" stroke="#333" stroke-width="1.2"/><line x1="300" y1="0" x2="0" y2="300" stroke="#333" stroke-width="1.2"/>'
    svg += '<rect x="0" y="0" width="300" height="300" fill="none" stroke="#333" stroke-width="2"/><path d="M150 0 L300 150 L150 300 L0 150 Z" fill="none" stroke="#333" stroke-width="1.2"/>'
    coords = [{"h":1,"nx":150,"ny":135,"px":150,"py":85},{"h":2,"nx":75,"ny":70,"px":50,"py":45},{"h":3,"nx":40,"ny":105,"px":25,"py":140},{"h":4
