# import streamlit
from datetime import datetime, date, timedelta
from resources import resource, list_inventory


class event:

    def __init__(self, type, beginning, end, needed_resources={}, description=None):
        self.type: str = type
        self.beginning: date = beginning
        self.end: date = end
        self.needed_resources: dict[resource:int] = needed_resources
        self.description = description

    def to_dict(self):
        return {
            "type": self.type,
            "beginning": self.beginning,
            "end": self.end,
            "needed_resources": self.needed_resources,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["type"],
            data["beginning"],
            data["end"],
            data["needed_resources"],
            data["description"],
        )

    def __str__(self):
        return f"{self.type} fijada desde {self.beginning} hasta {self.end}"


class planification:
    def __init__(self):
        self.events = []

    def add_event(self, inventory):
        event_type = input("Evento que desea crear: ")
        beginning = confirm_beginning(event_type)
        end = confirm_end(beginning, event_type)

        # Fragmento esencial bajo desarrollo
        needed_resources = {}
        answer = "si"

        while answer != "no":
            list_inventory(inventory)

            res = input("Que recurso desea asignar al evento: ")
            res = inventory[res]

            amount = self.assign_resource(res, beginning)
            if not amount:
                pass  # Que hare al recibir False?

            needed_resources[res] = amount
            answer = input("¿Desea asociar otro recurso al evento?:\n").lower()

        description = input(
            "A continuación puede añadir una descripción del evento.\n"
            "Si no le interesa hacerlo, presione 'Enter' sin escribir nada\n"
        )
        ########################################################################

        ei = event(event_type, beginning, end, needed_resources, description)

        self.events.append(ei)
        print("Se ha añadido el evento:")
        print(self.events[-1])
        self.events.sort(key=lambda e: e.beginning)
        print()

    def remove_event(self, index):
        if 0 <= index < len(self.events):
            return self.events.pop(index)
        else:
            print("Índice no válido.")

    def assign_resource(self, resour: resource, date: date):
        # Esto es teniendo en cuenta a date como fecha inicial
        for event in self.events:
            if event.beginning > date:
                break

            if event.end < date:
                continue

            if event.beginning <= date <= event.end:
                if resour in event.resources:
                    resour.in_use += event[resour]
        # Faltan hacer comprobaciones entre el final del evento que se está creando
        # e intervalos de otros eventos que vengan detras

        resour.set_available()
        if resour.available == 0:
            print("No hay disponibilidad de este recurso en estas fechas\n")
            return False

        amount = ask_amount(resour)
        resour.in_use = 0
        resour.set_available()
        return amount


def ask_amount(resour):
    amount = input("Que cantidad desea asociar: ")
    if amount > resour.available:
        print(
            f"No hay {amount} de {resour.name} disponibles en estas fechas\n"
            f"Solamente se dispone de {resour.available} {resour.name}"
        )
        ask_amount(resour)

    return amount


# Relacionado con las fechas a la hora de establecer un evento
def valid_date(posible_date):
    formats = ["%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d"]
    for format in formats:
        try:
            return datetime.strptime(posible_date, format).date()
        except ValueError:
            continue
    return False


def confirm_beginning(event_type: str):
    date = input(f"Fecha de inicio de la {event_type}: ")
    date = valid_date(date)

    if not date:
        print("El formato de la fecha no es válido\n" "Pruebe con (),() o ()")
        date = confirm_beginning(event_type)

    if date < date.today():
        print(
            "Error: Debe establecerse el inicio del evento para hoy, o para algún día posterior"
        )
        date = confirm_beginning(event_type)

    return date


def confirm_end(beginning: date, event_type: str):
    date = input(f"Fecha de terminación de la {event_type}: ")
    date = valid_date(date)

    if not date:
        print("El formato de la fecha no es válido\n" "Pruebe con (),() o ()")
        date = confirm_end(beginning, event_type)

    if date < beginning:
        print(
            "Error: El evento debe terminar el día en que comienza, o en algún día posterior"
        )
        date = confirm_end(beginning, event_type)

    return date


##############################################################
