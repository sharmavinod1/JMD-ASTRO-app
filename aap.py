import streamlit as st
import swisseph as swe
from datetime import datetime

# ऐप की मुख्य सेटिंग
st.set_page_config(page_title="Vinod Astro Software", layout="wide")

st.markdown("<h1 style='text-align: center; color: #d35400;'>Vinod Astrology Engine Pro</h1>", unsafe_allow_html=True)
st.write("---")

# --- इनपुट विभाग ---
with st.sidebar:
    st.header("जातक का विवरण")
    name = st.text_input("नाम", value="जातक")
    
    # तारीख की सीमा 1900-2100 तय की गई है
    dob = st.date_input(
        "जन्म तिथि", 
        value=datetime(1988, 1, 15),
        min_value=datetime(1900, 1, 1),
        max_value=datetime(2100, 12, 31)
    )
    
    tob = st.time_input("जन्म समय", value=datetime.strptime("12:00", "%H:%M").time())
    
    st.subheader("जन्म स्थान विवरण")
    city = st.text_input("शहर", value="Solapur")
    lat = st.number_input("अक्षांश (Latitude)", value=17.6599, format="%.4f")
    lon = st.number_input("रेखांश (Longitude)", value=75.9064, format="%.4f")
    st.info("गूगल से अक्षांश/रेखांश देखकर यहाँ अपडेट करें।")

# --- गणना इंजन ---
def draw_kundli(asc_sign, house_planets, chart_title):
    svg = f'<svg width="320" height="320" viewBox="0 0 300 300" style="display:block; margin:auto; background:#fff; border:2px solid #d35400; border-radius:10px;">'
    svg += '<line x1="0" y1="0" x2="300" y2="300" stroke="#333" stroke-width="1"/><line x1="300" y1="0" x2="0" y2="300" stroke="#333" stroke-width="1"/>'
    svg += '<rect x="0" y="0" width="300" height="300" fill="none" stroke="#333" stroke-width="2"/><path d="M150 0 L300 150 L150 300 L0 150 Z" fill="none" stroke="#333" stroke-width="1"/>'
    
    coords = [
        {"h":1, "nx":150, "ny":135, "px":150, "py":85}, {"h":2, "nx":75, "ny":70, "px":50, "py":45},
        {"h":3, "nx":40, "ny":105, "px":25, "py":140}, {"h":4, "nx":75, "ny":165, "px":50, "py":205},
        {"h":5, "nx":40, "ny":235, "px":25, "py":275}, {"h":6, "nx":75, "ny":275, "px":50, "py":295},
        {"h":7, "nx":150, "ny":215, "px":150, "py":265}, {"h":8, "nx":225, "ny":275, "px":250, "py":295},
        {"h":9, "nx":260, "ny":235, "px":275, "py":275}, {"h":10, "nx":225, "ny":165, "px":250, "py":205},
        {"h":11, "nx":260, "ny":105, "px":275, "py":140}, {"h":12, "nx":225, "ny":70, "px":250, "py":45}
    ]
    
    for c in coords:
        # राशि नंबर
        s_num = (asc_sign + c['h'] - 2) % 12 + 1
        svg += f'<text x="{c["nx"]}" y="{c["ny"]}" font-size="16" fill="#d35400" font-weight="bold" text-anchor="middle">{s_num}</text>'
        # ग्रह
        for i, p in enumerate(house_planets.get(c['h'], [])):
            svg += f'<text x="{c["px"]}" y="{c["py"]+(i*13)}" font-size="11" fill="#2c3e50" font-weight="bold" text-anchor="middle">{p}</text>'
    svg += "</svg>"
    return svg

# --- मुख्य कार्य ---
try:
    # IST to UTC (Timezone Correction)
    jd = swe.julday(dob.year, dob.month, dob.day, tob.hour + tob.minute/60.0 - 5.5)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # लग्न गणना
    res, ascmc = swe.houses_ex(jd, lat, lon, b'P')
    asc_deg = ascmc[0]
    asc_sign = int(asc_deg / 30) + 1
    
    # ग्रहों का डेटा निकालना
    planets_list = {"सूर्य": swe.SUN, "चन्द्र": swe.MOON, "मंगल": swe.MARS, "बुध": swe.MERCURY, 
                    "गुरु": swe.JUPITER, "शुक्र": swe.VENUS, "शनि": swe.SATURN, "राहु": swe.MEAN_NODE}
    
    d1_houses = {i: [] for i in range(1, 13)}
    d9_houses = {i: [] for i in range(1, 13)}
    planet_table = []

    for p_name, p_id in planets_list.items():
        p_res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
        lon_p = p_res[0]
        
        # D1 (लग्न कुण्डली)
        p_sign = int(lon_p / 30) + 1
        h_idx = (p_sign - asc_sign + 12) % 12 + 1
        d1_houses[h_idx].append(p_name)
        
        # D9 (नवमांश)
        d9_sign = int((lon_p % 30) * 9 / 30) % 12 + 1
        d9_houses[d9_sign].append(p_name)
        
        planet_table.append({"ग्रह": p_name, "राशि": int(lon_p/30)+1, "अंश (Degree)": f"{int(lon_p%30)}° {int((lon_p*60)%60)}'"})

    # केतु (राहु के ठीक सामने)
    ra_lon = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)[0][0]
    ke_lon = (ra_lon + 180) % 360
    d1_houses[(int(ke_lon/30)+1 - asc_sign + 12)%12+1].append("केतु")
    d9_houses[int((ke_lon % 30) * 9 / 30) % 12 + 1].append("केतु")

    # प्रदर्शन (Display Layout)
    colA, colB = st.columns(2)
    
    with colA:
        st.subheader("लग्न कुण्डली (D1)")
        st.markdown(draw_kundli(asc_sign, d1_houses, "Lagna Chart"), unsafe_allow_html=True)
    
    with colB:
        st.subheader("नवमांश कुण्डली (D9)")
        st.markdown(draw_kundli(1, d9_houses, "Navamsha Chart"), unsafe_allow_html=True) # Assumed D9 Mesh Lagna
        
    st.write("---")
    
    tab1, tab2 = st.tabs(["ग्रह स्पष्ट विवरण", "विंशोत्तरी महादशा"])
    
    with tab1:
        st.table(planet_table)
        
    with tab2:
        # नक्षत्र और दशा स्वामी
        mo_lon = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
        nak_no = int(mo_lon * 3 / 40)
        lords = ["केतु", "शुक्र", "सूर्य", "चन्द्र", "मंगल", "राहु", "गुरु", "शनि", "बुध"]
        st.write(f"**जन्म नक्षत्र:** {nak_no + 1}")
        st.write(f"**वर्तमान महादशा स्वामी:** {lords[nak_no % 9]}")

except Exception as e:
    st.error(f"गणना में त्रुटि: {e}")

st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>Designed for Vinod Jagdish Sharma</p>", unsafe_allow_html=True)
