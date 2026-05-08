import streamlit as st
import swisseph as swe
from datetime import datetime

# ऐप की सेटिंग
st.set_page_config(page_title="Vinod Astro Pro", layout="centered")
st.markdown("<h2 style='text-align:center; color:#d35400;'>Vinod Astrology Software</h2>", unsafe_allow_html=True)

# --- इनपुट सेक्शन ---
name = st.text_input("जातक का नाम")

col1, col2 = st.columns(2)
with col1:
    dob = st.date_input("जन्म तिथि")
    tob = st.time_input("जन्म समय")
with col2:
    # जन्म स्थान का कॉलम और कोऑर्डिनेट्स
    city = st.text_input("जन्म स्थान (शहर)", value="Solapur")
    lat = st.number_input("अक्षांश (Latitude)", value=17.6599, format="%.4f")
    lon = st.number_input("रेखांश (Longitude)", value=75.9064, format="%.4f")

st.caption("नोट: यदि शहर सोलापुर नहीं है, तो कृपया उस शहर के अक्षांश/रेखांश गूगल से देखकर यहाँ भरें।")

# --- कुण्डली बनाने का फंक्शन ---
def draw_chart(asc_sign, house_planets):
    svg = f'<svg width="300" height="300" viewBox="0 0 300 300" style="display:block; margin:auto; background:white; border:2px solid #333;">'
    svg += '<line x1="0" y1="0" x2="300" y2="300" stroke="#333" stroke-width="1.5"/><line x1="300" y1="0" x2="0" y2="300" stroke="#333" stroke-width="1.5"/>'
    svg += '<rect x="0" y="0" width="300" height="300" fill="none" stroke="#333" stroke-width="2"/><path d="M150 0 L300 150 L150 300 L0 150 Z" fill="none" stroke="#333" stroke-width="1.5"/>'
    
    coords = [
        {"h":1, "nx":150, "ny":135, "px":150, "py":85}, {"h":2, "nx":75, "ny":70, "px":50, "py":45},
        {"h":3, "nx":40, "ny":105, "px":25, "py":140}, {"h":4, "nx":75, "ny":165, "px":50, "py":205},
        {"h":5, "nx":40, "ny":235, "px":25, "py":275}, {"h":6, "nx":75, "ny":275, "px":50, "py":295},
        {"h":7, "nx":150, "ny":215, "px":150, "py":265}, {"h":8, "nx":225, "ny":275, "px":250, "py":295},
        {"h":9, "nx":260, "ny":235, "px":275, "py":275}, {"h":10, "nx":225, "ny":165, "px":250, "py":205},
        {"h":11, "nx":260, "ny":105, "px":275, "py":140}, {"h":12, "nx":225, "ny":70, "px":250, "py":45}
    ]
    for c in coords:
        s_num = (asc_sign + c['h'] - 2) % 12 + 1
        svg += f'<text x="{c["nx"]}" y="{c["ny"]}" font-size="14" fill="#d35400" font-weight="bold" text-anchor="middle">{s_num}</text>'
        for i, p in enumerate(house_planets.get(c['h'], [])):
            svg += f'<text x="{c["px"]}" y="{c["py"]+(i*12)}" font-size="10" fill="#333" text-anchor="middle">{p}</text>'
    svg += "</svg>"
    return svg

# --- मुख्य बटन ---
if st.button("सटीक कुण्डली और नवमांश देखें"):
    try:
        # गणना समय (IST to UTC सुधार)
        jd = swe.julday(dob.year, dob.month, dob.day, tob.hour + tob.minute/60.0 - 5.5)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # लग्न और घरों की गणना
        res, ascmc = swe.houses_ex(jd, lat, lon, b'P')
        asc_deg = ascmc[0]
        asc_sign = int(asc_deg / 30) + 1
        
        # ग्रहों का डेटा
        planets = {"सूर्य": swe.SUN, "चन्द्र": swe.MOON, "मंगल": swe.MARS, "बुध": swe.MERCURY, 
                   "गुरु": swe.JUPITER, "शुक्र": swe.VENUS, "शनि": swe.SATURN, "राहु": swe.MEAN_NODE}
        
        d1_houses = {i: [] for i in range(1, 13)}
        d9_houses = {i: [] for i in range(1, 13)}
        p_table = []

        for p_name, p_id in planets.items():
            p_res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
            lon_p = p_res[0]
            
            # D1 (लग्न)
            p_sign = int(lon_p / 30) + 1
            h_idx = (p_sign - asc_sign + 12) % 12 + 1
            d1_houses[h_idx].append(p_name)
            
            # D9 (नवमांश)
            d9_sign_total = int(lon_p * 9 / 30) % 12 + 1
            d9_houses[d9_sign_total].append(p_name)
            
            p_table.append({"ग्रह": p_name, "डिग्री": f"{int(lon_p%30)}° {int((lon_p*60)%60)}'"})

        # केतु को राहु के सामने जोड़ें
        ra_lon = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)[0][0]
        ke_lon = (ra_lon + 180) % 360
        d1_houses[(int(ke_lon/30)+1 - asc_sign + 12)%12+1].append("केतु")
        d9_houses[int(ke_lon * 9 / 30) % 12 + 1].append("केतु")

        # --- आउटपुट ---
        st.write(f"### जातक: {name} | स्थान: {city}")
        
        tab1, tab2, tab3 = st.tabs(["लग्न कुण्डली (D1)", "नवमांश (D9)", "ग्रह विवरण"])
        
        with tab1:
            st.markdown(draw_chart(asc_sign, d1_houses), unsafe_allow_html=True)
        with tab2:
            st.markdown(draw_chart(1, d9_houses), unsafe_allow_html=True) # D9 Mesh Lagna
        with tab3:
            st.table(p_table)

    except Exception as e:
        st.error(f"त्रुटि: {e}")

st.markdown("---")
st.markdown("<p style='text-align:center; font-size:12px;'>© 2026 Vinod Jagdish Sharma Astrology Engine</p>", unsafe_allow_html=True)
