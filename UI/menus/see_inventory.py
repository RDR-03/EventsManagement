import streamlit as st

inventory = st.session_state.inventory
schedule = st.session_state.schedule

if "changed_resource" not in st.session_state:
    st.session_state.changed_resource = False

if "increase_form" not in st.session_state:
    st.session_state.increase_form = False

if "decrease_form" not in st.session_state:
    st.session_state.decrease_form = False

if "message" not in st.session_state:
    st.session_state.message = None

if "conflictive_future_events" not in st.session_state:
    st.session_state.conflictive_future_events = None

st.title("Gestionar Inventario")

# Mensajes al usuario
if st.session_state.conflictive_future_events != None:
    st.warning(st.session_state.conflictive_future_events)
    st.session_state.conflictive_future_events = None

elif st.session_state.changed_resource:
    st.success(st.session_state.message)

elif not st.session_state.changed_resource and st.session_state.message != None:
    st.error(st.session_state.message)


# Representación visual del inventario
header = st.columns(2)
header[0].subheader("Recurso")
header[1].subheader("Cantidad total")
# header[3].subheader("Disponibilidad más próxima")

for key, value in inventory.items():
    row = st.columns(2)

    row[0].write(key)
    row[1].write(value.total_cuantity)
###################################################

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Aumentar cantidad", type="secondary"):
        st.session_state.decrease_form = False
        st.session_state.increase_form = True

with col2:
    if st.button("➖ Disminuir cantidad", type="secondary"):
        st.session_state.increase_form = False
        st.session_state.decrease_form = True

if st.session_state.increase_form:
    with st.form("select_resource_1"):
        selection = st.selectbox("Recurso a aumentar", inventory.keys())
        amount = st.number_input("Cantidad a aumentar", min_value=1, step=1)
        submitted = st.form_submit_button("Confirmar")

    if submitted:
        st.session_state.changed_resource = inventory[selection].increase_amount(amount)
        st.session_state.message = f"Se han incorporado {amount} {selection}"
        st.session_state.increase_form = False
        st.rerun()

if st.session_state.decrease_form:
    with st.form("select_resource_2"):
        selection = st.selectbox("Recurso a disminuir", inventory.keys())
        amount = st.number_input("Cantidad a disminuir", min_value=1, step=1)
        submitted = st.form_submit_button("Confirmar")

    if submitted:
        resource_selected = inventory[selection]
        conflictive_events = []

        # Para recalcular resource_availability correctamente
        resource_selected.total_cuantity -= amount

        for ev in schedule.events:

            if resource_selected in ev.needed_resources:
                start = ev.beginning
                end = ev.end

                available = schedule.resource_availability(
                    resource_selected, start, end
                )

                if available < ev.needed_resources[resource_selected]:
                    date = ev.beginning.strftime("%d/%m/%Y a las %H:%M")
                    conflictive_events.append(
                        f"**{ev.type}** (Programada para el {date})"
                    )

        resource_selected.total_cuantity += amount

        if conflictive_events:
            visual_list = "\n".join(conflictive_events)
            st.session_state.conflictive_future_events = (
                f"No dispondrá de la cantidad necesaria si descuenta del inventario "
                f"{amount} {resource_selected.name}, "
                f"para la realización de los siguientes eventos activos:\n\n{visual_list}\n\n"
                f"Por favor, revise la agenda o reabastezca el recurso para evitar problemas de disponibilidad."
            )
            st.session_state.changed_resource = False
            st.rerun()
        else:
            st.session_state.changed_resource = resource_selected.decrease_amount(
                amount
            )

        if st.session_state.changed_resource:
            st.session_state.message = f"Se han quitado {amount} {selection}"

        else:
            st.session_state.message = f"La cantidad de {selection} que se desea retirar supera la cantidad total"

        st.session_state.decrease_form = False
        st.rerun()
