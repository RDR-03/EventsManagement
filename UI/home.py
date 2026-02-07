import streamlit as st

if "menu" not in st.session_state:
    st.session_state.menu = "home"

menus = ["home", "event_creation", "see_inventory", "see_schedule"]


def go_to_menu():
    st.title("Gestor de eventos")
    st.header("Que desea hacer")

    if st.button("Crear evento"):
        st.session_state.menu = menus[1]
        st.rerun()

    if st.button("Ver inventario"):
        st.session_state.menu = menus[2]
        st.rerun()

    if st.button("Ver eventos planificados"):
        st.session_state.menu = menus[3]
        st.rerun()


def go_to_home():
    st.session_state.menu = "home"
    st.rerun()


menu = st.session_state.menu

home_page = st.Page(go_to_home, title="Inicio", icon=":material/logout:")
event_creation_page = st.Page(
    "menus/event_creation.py",
    title="Creación del evento",
    icon=":material/settings:",
)
see_inventory_page = st.Page("menus/see_inventory.py", title="Inventario")
see_schedule_page = st.Page("menus/see_schedule.py", title="Eventos Planificados")

if menu == "home":
    pg = st.navigation([st.Page(go_to_menu)])
if menu == "event_creation":
    pg = st.navigation([event_creation_page, home_page])
if menu == "see_schedule":
    pg = st.navigation([see_schedule_page, home_page])
if menu == "see_inventory":
    pg = st.navigation([see_inventory_page, home_page])

pg.run()
