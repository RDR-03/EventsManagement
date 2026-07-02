import streamlit as st
import pandas as pd

schedule = st.session_state.schedule
st.title("Eventos Planificados")

if "confirmation" not in st.session_state:
    st.session_state.confirmation = False

if "event_to_delete_id" not in st.session_state:
    st.session_state.event_to_delete_id = None

if "event_created" not in st.session_state:
    st.session_state.event_created = None

if st.session_state.confirmation and st.session_state.event_to_delete_id != None:
    id = st.session_state.event_to_delete_id
    eliminated_event = schedule.events.pop(id)

    st.success(f"Se ha removido el evento {eliminated_event.type} exitosamente")
    st.session_state.confirmation = False
    st.session_state.event_to_delete_id = None
    st.rerun()

# Mostrado del mensaje de evento creado
if st.session_state.event_created:
    st.success("Evento creado con éxito")
    st.write(st.session_state.event_message)

    st.session_state.event_created = None
    st.session_state.event_message = None

data_estructure = []
events_options = []

for i, event in enumerate(schedule.events):
    data = {}
    data["Evento"] = event.type
    data["Descipción"] = event.description
    data["Inicio"] = f"{event.beginning.date()} - {event.beginning.time()}"
    data["Final"] = f"{event.end.date()} - {event.end.time()}"
    data["Recursos asignados"] = ""

    for resource, amount in event.needed_resources.items():
        data["Recursos asignados"] += f"{resource.name}: {amount},\n"

    data_estructure.append(data)
    events_options.append(f"{i} - {event.type} ({event.beginning.date()})")

df = pd.DataFrame(data_estructure)
st.dataframe(df)


@st.dialog("Desea la eliminación de este evento")
def Ask_confirmation():
    if st.button("Sí, eliminar"):
        st.session_state.confirmation = True
        st.rerun()

    elif st.button("Cancelar"):
        st.session_state.confirmation = False
        st.session_state.event_to_delete_idx = None
        st.rerun()


if len(schedule.events) > 0:
    st.write("---")
    st.subheader("Gestionar planificación")

    selection = st.selectbox("Seleccione el evento que desea eliminar:", events_options)
    id_selected = int(selection.split(" - ")[0])

    if st.button("Eliminar evento seleccionado", type="primary"):
        st.session_state.event_to_delete_id = id_selected
        Ask_confirmation()
else:
    st.info("No hay eventos planificados.")
