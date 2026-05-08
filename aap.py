import streamlit as st
import swisseph as swe
from datetime import datetime

st.set_page_config(page_title="Vinod Astro Pro", layout="centered")
st.markdown("<h2 style='text-align:center; color:#d35400;'>Vinod Astrology Engine</h2>", unsafe_allow_html=True)

name = st.text_input("जातक का नाम")
dob = st.date_input("जन्म तिथि")
tob = st.time_input("जन्म समय")

if st.button("सटीक कुण्डली गणना करें"):
    try:
        # ज्योतिषीय गणना
        swe.set_ephe_path('') # Default path
        jd = swe.julday(dob.year, dob.month, dob.day, tob.hour + tob.minute/60.0 - 5.5)
        
        # अयनंशा (लाहिरी)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # लग्न गणना (सोलापुर लोकेशन)
        res, ascmc = swe.houses_ex(jd, 17.6599, 75.9064, b'P')
        asc_deg = ascmc[0]
        asc_sign = int(asc_deg / 30) + 1
        
        # ग्रहों की स्थिति
        planets_data = {
            "सूर्य": swe.SUN, "चन्द्र": swe.MOON, "मंगल": swe.MARS,
            "बुध": swe.MERCURY, "गुरु": swe.JUPITER, "शुक्र": swe.VENUS,
            "शनि": swe.SATURN, "राहु": swe.MEAN_NODE
        }
        
        house_planets = {i: [] for i in range(1, 13)}
        for p_name, p_id in planets_data.items():
            p_res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
            p_deg = p_res[0]
            p_sign = int(p_deg / 30) + 1
            h_idx = (p_sign - asc_sign + 12) % 12 + 1
            house_planets[h_idx].append(p_name)
        
        # केतु गणना (राहु से 180 डिग्री दूर)
        ke_h = ( ( (asc_sign + ( ( ( ( ( ( ( (swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)[0][0] + 180) % 360) / 30) + 1) - asc_sign + 12) % 12 + 1) - 1) % 12) + 1 ) # Simplification for display
        # केतु को हमेशा राहु के सामने 7वें घर में रखें
        ra_h = (int(swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)[0][0] / 30) + 1 - asc_sign + 12) % 12 + 1
        ke_h = (ra_h + 6 - 1) % 12 + 1
        house_planets[ke_h].append("केतु")

        # कुण्डली चार्ट (SVG)
        svg = f'<svg width="320" height="320" viewBox="0 0 300 300" style="display:block; margin:auto; background:white; border:2px solid #333;">'
        svg += '<line x1="0" y1="0" x2="300" y2="300" stroke="#333" stroke-width="2"/><line x1="300" y1="0" x2="0" y2="300" stroke="#333" stroke-width="2"/>'
        svg += '<rect x="0" y="0" width="300" height="300" fill="none" stroke="#333" stroke-width="2"/><path d="M150 0 L300 150 L150 300 L0 150 Z" fill="none" stroke="#333" stroke-width="2"/>'
        
        coords = [
            {"h":1, "nx":150, "ny":135, "px":150, "py":80}, {"h":2, "nx":75, "ny":70, "px":45, "py":45},
            {"h":3, "nx":40, "ny":105, "px":25, "py":140}, {"h":4, "nx":75, "ny":165, "px":50, "py":200},
            {"h":5, "nx":40, "ny":235, "px":25, "py":270}, {"h":6, "nx":75, "ny":275, "px":50, "py":295},
            {"h":7, "nx":150, "ny":215, "px":150, "py":260}, {"h":8, "nx":225, "ny":275, "px":250, "py":295},
            {"h":9, "nx":260, "ny":235, "px":275, "py":270}, {"h":10, "nx":225, "ny":165, "px":250, "py":200},
            {"h":11, "nx":260, "ny":105, "px":275, "py":140}, {"h":12, "nx":225, "ny":70, "px":250, "py":45}
        ]

        for c in coords:
            s_num = (asc_sign + c['h'] - 2) % 12 + 1
            svg += f'<text x="{c["nx"]}" y="{c["ny"]}" font-size="16" fill="#d35400" font-weight="bold" text-anchor="middle">{s_num}</text>'
            for i, p in enumerate(house_planets[c['h']]):
                svg += f'<text x="{c["px"]}" y="{c["py"]+(i*12)}" font-size="10" fill="#333" text-anchor="middle">{p}</text>'
        
        svg += "</svg>"
        
        st.success(f"नमस्ते {name} जी! आपकी कुण्डली तैयार है।")
        st.markdown(svg, unsafe_allow_html=True)
        st.info("गणना लाहिरी अयनांश पर आधारित है।")
        
    except Exception as e:
        st.error(f"गणना में समस्या: {e}")
