import streamlit as st
from datetime import datetime, timedelta
from core.events import event

inventory = st.session_state.inventory
schedule = st.session_state.schedule

# Inicializando las variables encargadas de mostrar mensaje al usuario
if "event_created" not in st.session_state:
    st.session_state.event_created = None
if "event_message" not in st.session_state:
    st.session_state.event_message = None

# Recordatorio de fechas sugeridas
if "suggested_start" not in st.session_state:
    st.session_state.suggested_start = datetime.now()
if "suggested_end" not in st.session_state:
    st.session_state.suggested_end = datetime.now() + timedelta(hours=1)
# Mensaje de fecha sugerida
if "suggested_message" not in st.session_state:
    st.session_state.suggested_message = None

# Mostrado de error después del rerun
if st.session_state.event_created == False:
    st.error(st.session_state.event_message)

    st.session_state.event_created = None
    st.session_state.event_message = None

# Diseño de la página
st.title("Crear un evento")

event_type = st.selectbox("Qué tipo de evento desea crear", ["Boda", "Cena", "Reunión"])
description = st.text_area("A continuación puede hacer una descripción del evento")
selections = st.multiselect("Seleccione los recursos a asignar", inventory)

needed_resources = {}

if selections:
    st.markdown("**Cantidad requerida**")

    for resource in selections:
        # El usuario elige interactivamente la cantidad exacta que necesita
        amount = st.number_input(
            f"Cantidad de {resource}",
            min_value=1,
            step=1,
            key=f"amount_{resource}",
        )
        # Se guarda inmediatamente el recurso y la cantidad elegida
        needed_resources[inventory[resource]] = amount

    # Opción de buscar hueco
    with st.expander("¿No sabe qué fechas elegir? Use el Asistente de Disponibilidad"):
        col_asist1, col_asist2 = st.columns(2)
        starting_date = col_asist1.datetime_input(
            "Buscar horario a partir de:",
            min_value=datetime.now(),
            key="search_from_date",
        )
        duration = col_asist2.number_input(
            "Duración estimada (horas):", min_value=1, step=1
        )

        if st.button("Buscar horario con disponibilidad de recursos"):
            posible_space = schedule.find_space(
                needed_resources, starting_date, duration
            )
            if posible_space is not None:
                sug_start, sug_end = posible_space

                st.session_state.suggested_start = sug_start
                st.session_state.suggested_end = sug_end
                st.session_state.suggested_message = f"✅ Se encontró el siguiente espacio:\
                      {sug_start.strftime('%d/%m/%Y %H:%M')} hasta {sug_end.strftime('%d/%m/%Y %H:%M')}"

                st.rerun()
            else:
                st.error(
                    "No hay disponibilidad conjunta para estos recursos en los próximos 45 días."
                )
    ##################################################################################

    st.write("---")

    if st.session_state.suggested_message is not None:
        st.success(st.session_state.suggested_message)

    # Elección personal de fechas
    start = st.datetime_input(
        f"Fecha de inicio de la {event_type}", value=st.session_state.suggested_start
    )
    if start < datetime.now().replace(minute=0, second=0, microsecond=0):
        st.error("El evento debe iniciar hoy o en un día posterior")

    end = st.datetime_input(
        f"Fecha de finalización de la {event_type}",
        value=st.session_state.suggested_end,
    )
    if end < start:
        st.error("El fin del evento debe ser igual o posterior a la fecha de inicio")

    valid_dates = True

    for resour, amount in needed_resources.items():
        availables = schedule.resource_availability(resour, start, end)
        if availables < amount:
            st.error(
                f"Ha solicitado {amount} {resour.name}, pero en estas fechas hay disponibles: {availables}"
            )
            valid_dates = False
        else:
            st.caption(
                f"✅ {amount} {resour.name} fueron asignados correctamente (Disponibles en total: {availables})"
            )

    if st.button("Confirmar evento"):
        if not valid_dates:
            st.error(
                "No puede registrar el evento por falta de disponibilidad en las fechas seleccionadas.\
                Ajuste las fechas o use el asistente."
            )
        else:
            posible_event = schedule.valid_event(
                event_type, start, end, needed_resources, description
            )
            if isinstance(posible_event, event):
                i = 0
                while i < len(schedule.events):
                    if posible_event.beginning < schedule.events[i].beginning:
                        schedule.events.insert(i, posible_event)
                        break
                    else:
                        i += 1

                if i == len(schedule.events):
                    schedule.events.append(posible_event)

                st.session_state.event_created = True
                st.session_state.event_message = posible_event
            else:
                st.session_state.event_created = False
                st.session_state.event_message = posible_event
                st.rerun()

            st.switch_page("UI/menus/see_schedule.py")
