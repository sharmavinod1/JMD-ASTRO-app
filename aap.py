import streamlit as st
import swisseph as swe
from datetime import datetime

# ऐप की मुख्य सेटिंग
st.set_page_config(page_title="Vinod Astro Pro", layout="wide")
st.markdown("<h1 style='text-align: center; color: #d35400;'>Vinod Astrology Software</h1>", unsafe_allow_html=True)

# --- प्रमुख शहरों का डेटाबेस ---
CITIES = {
    "Solapur": {"lat": 17.6599, "lon": 75.9064},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Pune": {"lat": 18.5204, "lon": 73.8567},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882},
    "Nashik": {"lat": 19.9975, "lon": 73.7898},
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "Indore": {"lat": 22.7196, "lon": 75.8577},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867}
}

with st.sidebar:
    st.header("जातक का विवरण")
    name = st.text_input("नाम", value="जातक")
    
    # तारीख चुनने का विकल्प (1900-2100)
    dob = st.date_input("जन्म तिथि", value=datetime(1988, 1, 15), 
                        min_value=datetime(1900, 1, 1), max_value=datetime(2100, 12, 31))
    
    # समय चुनने का आसान विकल्प
    tob = st.time_input("जन्म समय", value=datetime.strptime("12:00", "%H:%M").time())
    
    # शहर चुनने का ड्रॉपडाउन विकल्प
    city_choice = st.selectbox("शहर चुनें", options=list(CITIES.keys()))
    
    # चुने गए शहर के हिसाब से Lat/Long अपने आप भर जाएंगे
    lat = st.number_input("अक्षांश (Lat)", value=CITIES[city_choice]["lat"], format="%.4f")
    lon = st.number_input("रेखांश (Long)", value=CITIES[city_choice]["lon"], format="%.4f")

# --- कुण्डली बनाने का फंक्शन ---
def draw_kundli(asc_sign, house_planets):
    svg = f'<svg width="300" height="300" viewBox="0 0 300 300" style="display:block; margin:auto; background:#fff; border:2px solid #d35400;">'
    svg += '<line x1="0" y1="0" x2="300" y2="300" stroke="#333" stroke-width="1.5"/><line x1="300" y1="0" x2="0" y2="300" stroke="#333" stroke-width="1.5"/>'
    svg += '<rect x="0" y="0" width="300" height="300" fill="none" stroke="#333" stroke-width="2"/><path d="M150 0 L300 150 L150 300 L0 150 Z" fill="none" stroke="#333" stroke-width="1.5"/>'
    coords = [{"h":1,"nx":150,"ny":135,"px":150,"py":85},{"h":2,"nx":75,"ny":70,"px":50,"py":45},{"h":3,"nx":40,"ny":105,"px":25,"py":140},{"h":4,"nx":75,"ny":165,"px":50,"py":205},{"h":5,"nx":40,"ny":235,"px":25,"py":275},{"h":6,"nx":75,"ny":275,"px":50,"py":295},{"h":7,"nx":150,"ny":215,"px":150,"py":265},{"h":8,"nx":225,"ny":275,"px":250,"py":295},{"h":9,"nx":260,"ny":235,"px":275,"py":275},{"h":10,"nx":225,"ny":165,"px":250,"py":205},{"h":11,"nx":260,"ny":105,"px":275,"py":140},{"h":12,"nx":225,"ny":70,"px":250,"py":45}]
    for c in coords:
        s_num = (asc_sign + c['h'] - 2) % 12 + 1
        svg += f'<text x="{c["nx"]}" y="{c["ny"]}" font-size="16" fill="#d35400" font-weight="bold" text-anchor="middle">{s_num}</text>'
        for i, p in enumerate(house_planets.get(c['h'], [])):
            svg += f'<text x="{c["px"]}" y="{c["py"]+(i*13)}" font-size="11" fill="#333" font-weight="bold" text-anchor="middle">{p}</text>'
    return svg + "</svg>"

try:
    # गणना शुरू (IST to UTC)
    utc_time = tob.hour + tob.minute/60.0 - 5.5
    jd = swe.julday(dob.year, dob.month, dob.day, utc_time)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # लग्न
    res, ascmc = swe.houses_ex(jd, lat, lon, b'P')
    asc_deg = ascmc[0]
    asc_sign = int(asc_deg / 30) + 1
    
    planets = {"सूर्य": swe.SUN, "चन्द्र": swe.MOON, "मंगल": swe.MARS, "बुध": swe.MERCURY, "गुरु": swe.JUPITER, "शुक्र": swe.VENUS, "शनि": swe.SATURN, "राहु": swe.MEAN_NODE}
    d1_houses = {i: [] for i in range(1, 13)}
    
    for p_name, p_id in planets.items():
        p_res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
        p_sign = int(p_res[0] / 30) + 1
        h_idx = (p_sign - asc_sign + 12) % 12 + 1
        d1_houses[h_idx].append(p_name)

    # केतु
    ra_lon = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)[0][0]
    ke_sign = int(((ra_lon + 180) % 360) / 30) + 1
    d1_houses[(ke_sign - asc_sign + 12) % 12 + 1].append("केतु")

    # प्रदर्शन
    st.write(f"### जातक: {name} | स्थान: {city_choice}")
    st.markdown(draw_kundli(asc_sign, d1_houses), unsafe_allow_html=True)
    st.info(f"गणना {city_choice} के अक्षांश {lat} और रेखांश {lon} पर आधारित है।")

except Exception as e:
    st.error(f"त्रुटि: {e}")
