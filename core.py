from datetime import datetime
import os
import json

Events = ("evento1", "evento2", "evento3", "evento4", "evenrto5")
Resources = {"A": 3, "B": 6, "C": 7}
Planification = {}
plan_ID = 1


def establish_event():
    global plan_ID

    # Modificar para que el usuario decida que tipo de evento poner
    # No esta todavia por no tener claro logica-visual aún
    event = 0
    date = datetime()

    Planification[plan_ID] = {
        "Evento": Events[event],
        "Fecha": date,
        "Estado": "Pendiente",
    }
    plan_ID += 1


def add_resources():
    # Decision a cargo del usuario
    selection = "A"
    amount = 3

    Resources[selection] += amount


def show_planification():
    if not Planification:
        print("No hay eventos planificados")
    else:
        for event in Planification:
            print(event)


# Persistencia de datos:
FilePath = "planing.json"


def SaveData():
    data = {
        "events": Events,
        "planification": Planification,
        "resources": Resources,
        "plan_ID": plan_ID,
    }
    with open(FilePath, "w") as f:
        json.dump(data, f, indent=4)


def LoadData():
    global plan_ID, Planification, Resources, Events

    if not os.path.exists(FilePath):
        print("No hay un archivo del cual cargar datos")

    try:
        with open(FilePath, "r") as f:
            data = json.load(f)
            Planification = data.get("planification", {})
            Resources = data.get("resources")
            plan_ID = data.get("plan_ID", 1)
            Events = data.get("Events")

            Resources = {k: int(v) for k, v in Resources.items()}
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
