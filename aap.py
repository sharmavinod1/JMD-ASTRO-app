import streamlit as st
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

st.set_page_config(page_title="Vinod Astro", layout="centered")
st.markdown("<h2 style='text-align: center; color: #d35400;'>Vinod Astrology Engine</h2>", unsafe_allow_html=True)

name = st.text_input("जातक का नाम")
dob = st.date_input("जन्म तिथि")
tob = st.time_input("जन्म समय")

if st.button("सटीक कुण्डली देखें"):
    try:
        dt = Datetime(dob.strftime('%Y/%m/%d'), tob.strftime('%H:%M'), '+05:30')
        pos = GeoPos(17.6599, 75.9064) # सोलापुर
        chart = Chart(dt, pos)
        
        def get_s(obj):
            return int(((obj.lon - 24.08) % 360) / 30) + 1

        asc = get_s(chart.get(const.ASC))
        st.success(f"नमस्ते {name} जी! आपकी लग्न राशि संख्या {asc} है।")
        st.write("गणना पूरी हुई।")
    except Exception as e:
        st.error(f"त्रुटि: {e}")
