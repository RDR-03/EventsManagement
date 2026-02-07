from events import event
from planification import planification
from resources import resource, make_inventory
from datetime import date, datetime
import os, json


DataShow = resource("Datashow", 2)
Pantalla_tela = resource("Pantallas tela")
Salon = resource("Salones", 3)
Tv = resource("Tv's", 10)
Laptop = resource("Laptops", 3)
Tecnico_AV = resource("Técnicos AV", 2)
Coffee_break = resource("Coffee break", 5)
Dependiente_gastronomico = resource("Dependientes gastronómicos", 6)
Paquete_boda = resource("Paquetes de boda", 2)

Inventory = make_inventory(
    DataShow,
    Pantalla_tela,
    Tv,
    Laptop,
    Tecnico_AV,
    Coffee_break,
    Dependiente_gastronomico,
    Paquete_boda,
)

# Persistencia con Json
ResourcesPath = "./data/Inventory.json"
EventsPath = "./data/Events.json"


def SaveData(inventory: dict, planification: list = None):
    inventory_json = []
    for value in inventory.values():
        inventory_json.append(value.to_dict())

    with open(ResourcesPath, "w") as r:
        json.dump(inventory_json, r, indent=2)

    schedule_json = []
    for event in planification.events:
        schedule_json.append(event.to_dict())

    with open(EventsPath, "w") as e:
        json.dump(schedule_json, e, indent=2)


def LoadEvents():
    if not os.path.exists(EventsPath):
        print("No hay un archivo del cual cargar datos")
        return False

    plan = planification()

    with open(EventsPath, "r") as f:
        events_list = json.load(f)
        for data in events_list:
            plan.events.append(event.from_dict(data))

    plan.events.sort(key=lambda e: e.beginning)
    return plan


def LoadResources():
    if not os.path.exists(ResourcesPath):
        print("No hay un archivo del cual cargar datos")

    Inventory = {}

    with open(ResourcesPath, "r") as f:
        resources_list = json.load(f)
        for data in resources_list:
            resour = resource.from_dict(data)
            Inventory[resour.name] = resour

    return Inventory


e1 = event("boda", datetime.now(), datetime.now())
plan = planification()
