import streamlit as st
from UI.home import inventory

if "changed_resource" not in st.session_state:
    st.session_state.changed_resource = False

if "increase_form" not in st.session_state:
    st.session_state.increase_form = False

if "decrease_form" not in st.session_state:
    st.session_state.decrease_form = False

if "message" not in st.session_state:
    st.session_state.message = None

st.title("Gestionar Inventario")

# Mensajes al usuario
if st.session_state.changed_resource:
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
        st.session_state.changed_resource = inventory[selection].decrease_amount(amount)
        st.session_state.decrease_form = False

        if st.session_state.changed_resource:
            st.session_state.message = f"Se han quitado {amount} {selection}"
        else:
            st.session_state.message = f"La cantidad de {selection} que se desea retirar supera la cantidad total"
        st.rerun()
