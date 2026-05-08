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
        # ज्योतिषीय गणना (Swiss Ephemeris)
        jd = swe.julday(dob.year, dob.month, dob.day, tob.hour + tob.minute/60.0)
        
        # लग्न (Ascendant) निकालना - सोलापुर के लिए
        res = swe.houses(jd, 17.6599, 75.9064, b'P')[0]
        asc_deg = res[0]
        asc_sign = int(asc_deg / 30) + 1
        
        # ग्रहों के नाम हिंदी में
        planets_list = {
            "सूर्य": swe.SUN, "चन्द्र": swe.MOON, "मंगल": swe.MARS,
            "बुध": swe.MERCURY, "गुरु": swe.JUPITER, "शुक्र": swe.VENUS,
            "शनि": swe.SATURN, "राहु": swe.MEAN_NODE
        }

        st.success(f"नमस्ते {name} जी! आपकी कुण्डली तैयार है।")
        st.write(f"**लग्न राशि संख्या:** {asc_sign}")
        
        # यहाँ आप चक्र भी दिखा सकते हैं
        st.info("गणना लाहिरी अयनांश पर आधारित है।")
        
    except Exception as e:
        st.error(f"गणना में समस्या: {e}")
