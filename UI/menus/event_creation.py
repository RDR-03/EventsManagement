import streamlit as st
from datetime import datetime
from UI.home import inventory, schedule, go_to_home
from core.planification import planification
from core.events import event

st.title("Establecer un evento")

event_type = st.selectbox("Que tipo de evento desea crear", ["Boda", "Cena", "Reunion"])
start = st.datetime_input(f"Fecha de inicio de la {event_type}")

if start < datetime.now().replace(minute=0, second=0, microsecond=0):
    st.error("El evento debe iniciar hoy o en un día posterior")

end = st.datetime_input(f"Fecha de finalización de la {event_type}")

if end < start:
    st.error("El fin del evento debe ser igual o posterior a la fecha de inicio")

description = st.text_area("A continuación puede hacer una descripción del evento")

selections = st.multiselect("Seleccione los recursos a asignar", inventory)

if "needed_resources" not in st.session_state:
    st.session_state.needed_resources = {}
needed_resources = st.session_state.needed_resources

header = st.columns(2)
header[0].subheader("Recurso")
header[1].subheader("Disponibilidad")

with st.form("select resource"):
    for resource in selections:
        row_i = st.columns(2)

        amount = row_i[0].number_input(f"Cantidad de {resource} a asignar", step=1)
        disponibility = row_i[1].text(
            schedule.resource_availabilty(resource, start, end)
        )

        needed_resources[inventory[resource]] = amount

    posible_event = schedule.valid_event(
        event_type, start, end, needed_resources, description
    )

    submitted = st.form_submit_button("Confirmar recursos")

    if submitted:
        if type(posible_event) == event:
            schedule.events.append(posible_event)
            st.success("Evento creado con exito")
            st.write(posible_event)

        else:
            st.error(posible_event)
