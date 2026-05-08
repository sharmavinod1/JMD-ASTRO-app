import streamlit as st
import swisseph as swe
from datetime import datetime

# ऐप की मुख्य सेटिंग
st.set_page_config(page_title="Vinod Astro Pro", layout="wide")
st.markdown("<h1 style='text-align: center; color: #d35400;'>Vinod Astrology Software Pro</h1>", unsafe_allow_html=True)

# --- इनपुट विभाग ---
with st.sidebar:
    st.header("जातक का विवरण")
    name = st.text_input("जातक का नाम", value="विनोद")
    
    # 1. तारीख (1900-2100)
    dob = st.date_input("जन्म तिथि", value=datetime(1988, 1, 15), 
                        min_value=datetime(1900, 1, 1), max_value=datetime(2100, 12, 31))
    
    # 2. समय का मैनुअल इनपुट (यहाँ आप 2:50, 2:51 कुछ भी डाल सकते हैं)
    time_str = st.text_input("जन्म समय (HH:MM प्रारूप में)", value="02:50")
    try:
        tob = datetime.strptime(time_str, "%H:%M").time()
    except:
        st.error("समय का प्रारूप सही डालें (जैसे 02:50)")
        tob = datetime.strptime("00:00", "%H:%M").time()

    # 3. जन्म स्थान (मैनुअल अक्षांश/रेखांश)
    st.subheader("जन्म स्थान (Coordinates)")
    city = st.text_input("शहर का नाम", value="Solapur")
    lat = st.number_input("अक्षांश (Latitude)", value=17.6599, format="%.4f")
    lon = st.number_input("रेखांश (Longitude)", value=75.9064, format="%.4f")

# --- डिग्री को अंश-कला-विकला में बदलने का फंक्शन ---
def format_deg(decimal_deg):
    d = int(decimal_deg)
    m = int((decimal_deg - d) * 60)
    s = int((decimal_deg - d - m/60) * 3600)
    return f"{d % 30}° {m}' {s}\""

# --- कुण्डली चार्ट का फंक्शन ---
def draw_kundli(asc_sign, house_planets):
    svg = f'<svg width="350" height="350" viewBox="0 0 300 300" style="display:block; margin:auto; background:#fff; border:2px solid #d35400;">'
    svg += '<line x1="0" y1="0" x2="300" y2="300" stroke="#333" stroke-width="1.5"/><line x1="300" y1="0" x2="0" y2="300" stroke="#333" stroke-width="1.5"/>'
    svg += '<rect x="0" y="0" width="300" height="300" fill="none" stroke="#333" stroke-width="2"/><path d="M150 0 L300 150 L150 300 L0 150 Z" fill="none" stroke="#333" stroke-width="1.5"/>'
    coords = [{"h":1,"nx":150,"ny":135,"px":150,"py":85},{"h":2,"nx":75,"ny":70,"px":50,"py":45},{"h":3,"nx":40,"ny":105,"px":25,"py":140},{"h":4,"nx":75,"ny":165,"px":50,"py":205},{"h":5,"nx":40,"ny":235,"px":25,"py":275},{"h":6,"nx":75,"ny":275,"px":50,"py":295},{"h":7,"nx":150,"ny":215,"px":150,"py":265},{"h":8,"nx":225,"ny":275,"px":250,"py":295},{"h":9,"nx":260,"ny":235,"px":275,"py":275},{"h":10,"nx":225,"ny":165,"px":250,"py":205},{"h":11,"nx":260,"ny":105,"px":275,"py":140},{"h":12,"nx":225,"ny":70,"px":250,"py":45}]
    for c in coords:
        s_num = (asc_sign + c['h'] - 2) % 12 + 1
        svg += f'<text x="{c["nx"]}" y="{c["ny"]}" font-size="16" fill="#d35400" font-weight="bold" text-anchor="middle">{s_num}</text>'
        for i, p in enumerate(house_planets.get(c['h'], [])):
            svg += f'<text x="{c["px"]}" y="{c["py"]+(i*13)}" font-size="11" fill="#333" font-weight="bold" text-anchor="middle">{p}</text>'
    return svg + "</svg>"

# --- मुख्य गणना इंजन ---
try:
    utc_time = tob.hour + tob.minute/60.0 - 5.5
    jd = swe.julday(dob.year, dob.month, dob.day, utc_time)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # लग्न स्पष्ट
    res, ascmc = swe.houses_ex(jd, lat, lon, b'P')
    asc_deg = ascmc[0]
    asc_sign = int(asc_deg / 30) + 1
    
    planets = {"सूर्य": swe.SUN, "चन्द्र": swe.MOON, "मंगल": swe.MARS, "बुध": swe.MERCURY, 
               "गुरु": swe.JUPITER, "शुक्र": swe.VENUS, "शनि": swe.SATURN, "राहु": swe.MEAN_NODE}
    
    d1_houses = {i: [] for i in range(1, 13)}
    table_data = []

    # लग्न की जानकारी टेबल में जोड़ें
    table_data.append({"वस्तु": "लग्न (Ascendant)", "राशि": asc_sign, "अंश-कला-विकला": format_deg(asc_deg)})

    for p_name, p_id in planets.items():
        p_res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
        lon_p = p_res[0]
        p_sign = int(lon_p / 30) + 1
        h_idx = (p_sign - asc_sign + 12) % 12 + 1
        d1_houses[h_idx].append(p_name)
        
        table_data.append({"वस्तु": p_name, "राशि": p_sign, "अंश-कला-विकला": format_deg(lon_p)})

    # केतु स्पष्ट
    ra_lon = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)[0][0]
    ke_lon = (ra_lon + 180) % 360
    ke_sign = int(ke_lon / 30) + 1
    d1_houses[(ke_sign - asc_sign + 12) % 12 + 1].append("केतु")
    table_data.append({"वस्तु": "केतु", "राशि": ke_sign, "अंश-कला-विकला": format_deg(ke_lon)})

    # --- आउटपुट प्रदर्शन ---
    st.write(f"### जातक: {name} | जन्म समय: {time_str} | शहर: {city}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("लग्न कुण्डली (D1)")
        st.markdown(draw_kundli(asc_sign, d1_houses), unsafe_allow_html=True)
    
    with col2:
        st.subheader("ग्रह स्पष्ट (Detailed Degrees)")
        st.table(table_data)

    st.info("यह गणना लाहिरी अयनांश (Lahiri Ayanamsa) पर आधारित है। अंश-कला-विकला पूरी तरह स्पष्ट हैं।")

except Exception as e:
    st.error(f"त्रुटि: {e}")
