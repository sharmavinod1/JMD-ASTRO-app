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
        # ज्योतिषीय गणना सेटअप
        jd = swe.julday(dob.year, dob.month, dob.day, tob.hour + tob.minute/60.0 - 5.5)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        # लग्न गणना (सोलापुर)
        res, ascmc = swe.houses_ex(jd, 17.6599, 75.9064, b'P')
        asc_deg = ascmc[0]
        asc_sign = int(asc_deg / 30) + 1
        
        # ग्रहों की लिस्ट
        planets_data = {
            "सूर्य": swe.SUN, "चन्द्र": swe.MOON, "मंगल": swe.MARS,
            "बुध": swe.MERCURY, "गुरु": swe.JUPITER, "शुक्र": swe.VENUS,
            "शनि": swe.SATURN, "राहु": swe.MEAN_NODE
        }
        
        house_planets = {i: [] for i in range(1, 13)}
        
        # राहु की स्थिति पहले निकालें ताकि केतु बैठा सकें
        ra_res, _ = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)
        ra_sign = int(ra_res[0] / 30) + 1
        ra_h = (ra_sign - asc_sign + 12) % 12 + 1
        house_planets[ra_h].append("राहु")
        
        # केतु (राहु से ठीक सामने 7वां घर)
        ke_h = (ra_h + 6 - 1) % 12 + 1
        house_planets[ke_h].append("केतु")

        # बाकी ग्रहों को बैठाना
        for p_name, p_id in planets_data.items():
            if p_name == "राहु": continue
            p_res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
            p_sign = int(p_res[0] / 30) + 1
            h_idx = (p_sign - asc_sign + 12) % 12 + 1
            house_planets[h_idx].append(p_name)
        
        # कुण्डली का डायमंड चार्ट (SVG)
        svg = f'<svg width="320" height="320" viewBox="0 0 300 300" style="display:block; margin:auto; background:white; border:2px solid #333;">'
        svg += '<line x1="0" y1="0" x2="300" y2="300" stroke="#333" stroke-width="2"/>'
        svg += '<line x1="300" y1="0" x2="0" y2="300" stroke="#333" stroke-width="2"/>'
        svg += '<rect x="0" y="0" width="300" height="300" fill="none" stroke="#333" stroke-width="2"/>'
        svg += '<path d="M150 0 L300 150 L150 300 L0 150 Z" fill="none" stroke="#333" stroke-width="2"/>'
        
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
            svg += f'<text x="{c["nx"]}" y="{c["ny"]}" font-size="16" fill="#d35400" font-weight="bold" text-anchor="middle">{s_num}</text>'
            for i, p in enumerate(house_planets[c['h']]):
                y_off = c['py'] + (i * 13)
                svg += f'<text x="{c["px"]}" y="{y_off}" font-size="11" fill="#2c3e50" font-weight="bold" text-anchor="middle">{p}</text>'
        
        svg += "</svg>"
        
        st.success(f"नमस्ते {name} जी! आपकी कुण्डली तैयार है।")
        st.markdown(svg, unsafe_allow_html=True)
        st.info("स्थान: सोलापुर (महाराष्ट्र) | अयनांश: लाहिरी")
        
    except Exception as e:
        st.error(f"गणना में समस्या: {e}")

st.markdown("<p style='text-align:center; color:gray; font-size:10px;'>Developed by Vinod Jagdish Sharma</p>", unsafe_allow_html=True)
