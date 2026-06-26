import streamlit as st
import os, sys

parent_dir = os.path.dirname(os.path.abspath("home.py"))
sys.path.append(parent_dir)

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
###################################################################


if "menu" not in st.session_state:
    st.session_state.menu = "home"

menus = ["home", "event_creation", "see_inventory", "see_schedule"]


def go_to_menu():
    st.title("Gestor de eventos", text_alignment="center")
    st.header("¿Qué desea hacer?")

    if st.button("Crear evento"):
        st.session_state.menu = menus[1]
        st.rerun()

    if st.button("Gestionar inventario"):
        st.session_state.menu = menus[2]
        st.rerun()

    if st.button("Ver eventos planificados"):
        st.session_state.menu = menus[3]
        st.rerun()

    if st.button("Guardar datos"):
        SaveData(inventory, schedule)
        st.success("Datos guardados correctamente")
        st.rerun()


def go_to_home():
    st.session_state.menu = "home"
    st.rerun()


menu = st.session_state.menu

home_page = st.Page(go_to_home, title="Inicio", icon=":material/logout:")
event_page = st.Page(
    "menus/event_creation.py",
    title="Creación de evento",
    icon=":material/settings:",
)
schedule_page = st.Page("menus/see_schedule.py", title="Eventos Planificados")
inventory_page = st.Page("menus/see_inventory.py", title="Inventario")

if menu == "home":
    pg = st.navigation([st.Page(go_to_menu)])
elif menu == "event_creation":
    pg = st.navigation([event_page, home_page])
elif menu == "see_schedule":
    pg = st.navigation([schedule_page, home_page])
elif menu == "see_inventory":
    pg = st.navigation([inventory_page, home_page])

pg.run()
