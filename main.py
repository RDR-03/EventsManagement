import streamlit as st
from core._init_ import LoadEvents, LoadResources, SaveData, Inventory
from core.planification import planification

# Cargar datos
if "initialized" not in st.session_state:
    st.session_state.initialized = True

    schedule = LoadEvents()
    if schedule == False:
        st.write("No hay archivo desde donde cargar una planificación")
        schedule = planification()

    inventory = LoadResources()
    if inventory == False:
        st.write("Cargando el inventario base")
        inventory = Inventory

    st.session_state.schedule = schedule
    st.session_state.inventory = inventory

schedule = st.session_state.schedule
inventory = st.session_state.inventory
##################################################################


# Diseño de la pantalla inicial
def home_page():
    st.title("Gestor de Eventos")
    st.subheader("¡Bienvenido al sistema de planificación!")
    st.write(
        "Utilice la barra lateral de la izquierda para navegar entre las distintas herramientas."
    )

    st.write("---")
    st.write("Recuerde guardar sus cambios antes de cerrar la aplicación.")
    if st.button("💾 Guardar todos los datos actuales", type="primary"):
        SaveData(st.session_state.inventory, st.session_state.schedule)
        st.success("¡Los datos se han guardado correctamente en el sistema!")


welcome_page = st.Page(home_page, title="Inicio", icon="🏠")

event_page = st.Page("UI/menus/event_creation.py", title="Crear Evento", icon="📅")

inventory_page = st.Page(
    "UI/menus/see_inventory.py", title="Gestionar Inventario", icon="📦"
)

schedule_page = st.Page(
    "UI/menus/see_schedule.py", title="Eventos Planificados", icon="📋"
)

options = st.navigation([welcome_page, event_page, inventory_page, schedule_page])
options.run()
