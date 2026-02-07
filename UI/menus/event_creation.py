import streamlit as st
from datetime import datetime

st.title("Establecer un evento")

event_type = st.selectbox("Que tipo de evento desea crear", ["Boda", "Cena", "Reunion"])
start = st.date_input(f"Fecha de inicio de la {event_type}")

if start < datetime.now().replace(second=0, microsecond=0):
    st.error("El evento debe iniciar hoy o en un día posterior")

end = st.date_input(f"Fecha de finalización de la {event_type}")

if end < start:
    st.error("El fin del evento debe ser igual o posterior a la fecha de inicio")

description = st.text_area("A continuación puede hacer una descripción del evento")
