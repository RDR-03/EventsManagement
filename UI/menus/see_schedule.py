import streamlit as st
import pandas as pd
from UI.home import schedule

st.title("Eventos Planificados")

if "confirmation" not in st.session_state:
    st.session_state.confirmation = False

if st.session_state.confirmation:
    schedule.remove_event()
    st.success("Se ha removido el evento exitosamente")
    st.session_state.confirmation = False

data_estructure = []
for event in schedule.events:
    data = {}
    data["Evento"] = event.type
    data["Descipción"] = event.description
    data["Inicio"] = f"{event.beginning.date()} - {event.beginning.time()}"
    data["Final"] = f"{event.end.date()} - {event.end.time()}"

    data_estructure.append(data)

df = pd.DataFrame(data_estructure)
st.dataframe(df)


@st.dialog("Desea la eliminación de este evento")
def Ask_confirmation():
    if st.button("Sí"):
        st.session_state.confirmation = True
        st.rerun()

    elif st.button("Cancelar"):
        st.session_state.confirmation = False
        st.rerun()


remove = st.button("Eliminar evento")
if remove:
    Ask_confirmation()
