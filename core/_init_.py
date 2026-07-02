from core.events import event
from core.planification import planification
from core.resources import resource, make_inventory
import os, json


DataShow = resource("Datashow", 2)
Pantalla_tela = resource("Pantallas tela")
Salon = resource("Salones", 5)
Tv = resource("Tv's", 8)
Laptop = resource("Laptops", 3)
Microfono = resource("Micrófonos", 11)
Tecnico_AV = resource("Técnicos AV", 4)
Coffee_break = resource("Coffee break", 10)
Dependiente_gastronomico = resource("Dependientes gastronómicos", 15)
Paquete_boda = resource("Paquetes de boda", 2)

# Reglas definidas para los recursos del dominio
Coffee_break.dependant_on(Dependiente_gastronomico, amount=2)
Pantalla_tela.dependant_on(DataShow)
DataShow.dependant_on(Pantalla_tela)
DataShow.dependant_on(Tecnico_AV)
Microfono.dependant_on(Tecnico_AV)

resource.establish_conflict(Tv, DataShow)
##############################################################

Inventory = make_inventory(
    DataShow,
    Pantalla_tela,
    Salon,
    Tv,
    Laptop,
    Microfono,
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

    return True


def LoadEvents():
    if not os.path.exists(EventsPath):
        return False

    plan = planification()

    with open(EventsPath, "r") as f:
        events_list = json.load(f)
        for event_in_dict in events_list:

            # Convetir la llave de str a resource
            needed = {}
            for resource, amount in event_in_dict["needed_resources"].items():
                needed[Inventory[resource]] = amount
            event_in_dict["needed_resources"] = needed
            #########################################################

            plan.events.append(event.from_dict(event_in_dict))

    plan.events.sort(key=lambda e: e.beginning)
    return plan


def LoadResources():
    if not os.path.exists(ResourcesPath):
        return False

    Inventory = {}

    with open(ResourcesPath, "r") as f:
        resources_list = json.load(f)
        for data in resources_list:
            resour = resource.from_dict(data)
            Inventory[resour.name] = resour

    return Inventory
