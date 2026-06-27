import streamlit as st
from datetime import datetime
from core.events import event

inventory = st.session_state.inventory
schedule = st.session_state.schedule

# Inicializando las variables encargadas de mostrar mensaje al usuario
if "event_created" not in st.session_state:
    st.session_state.event_created = None
if "event_message" not in st.session_state:
    st.session_state.event_message = None

# Mostrado del mensaje después del rerun
if st.session_state.event_created:
    st.success("Evento creado con exito")
    st.write(st.session_state.event_message)

    st.session_state.event_created = None
    st.session_state.event_message = None

elif st.session_state.event_created == False:
    st.error(st.session_state.event_message)

# Diseño de la página
st.title("Crear un evento")

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
        row = st.columns(2)

        disponibility = row[1].text(
            schedule.resource_availabilty(inventory[resource], start, end)
        )
        amount = row[0].number_input(
            f"Cantidad de {resource} a asignar",
            min_value=1,
            step=1,
            key=f"amt_{resource}",
        )
        needed_resources[inventory[resource]] = amount

    submitted = st.form_submit_button("Confirmar recursos")

if submitted:
    posible_event = schedule.valid_event(
        event_type, start, end, needed_resources, description
    )

    if isinstance(posible_event, event):
        schedule.events.append(posible_event)
        st.session_state.event_created = True
        st.session_state.event_message = posible_event
    else:
        st.session_state.event_created = False
        st.session_state.event_message = posible_event

    st.rerun()
