# import streamlit
from datetime import datetime, date
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

            option = input("Que recurso desea asignar al evento: ")
            res = inventory[option]

            amount = self.check_resource(res, beginning, end)
            if not amount:
                print(
                    "No se puede establecer el evento con los recursos solicitados las fechas especificadas"
                )
                continue  # si el usuario deseara seguir planificando

            needed_resources[res] = amount
            answer = input("¿Desea asociar otro recurso al evento?:\n").lower()

        description = input(
            "A continuación puede añadir una descripción del evento.\n"
            "Si no le interesa hacerlo, presione 'Enter' sin escribir nada\n"
        )
        ########################################################################

        ei = event(event_type, beginning, end, needed_resources, description)
        self.events.append(ei)
        self.events.sort(key=lambda e: e.beginning)

        print("Se ha añadido el evento:")
        print(ei)
        print()

    def remove_event(self, index):
        if 0 <= index < len(self.events):
            return self.events.pop(index)
        else:
            print("Índice no válido.")

    def check_resource(self, resour: resource, beginning: date, end: date, amount=None):
        last_seen_event = 0
        for i in range(len(self.events)):
            if self.events[i].end < beginning:
                # No interesa el evento que se esta analizando si termina
                # antes del inicio del evento que se desea establecer
                continue

            if self.events[i].beginning > beginning:
                break

            if self.events[i].beginning <= beginning <= self.events[i].end:
                if resour in self.events[i].needed_resources:
                    resour.in_use += self.events[i].needed_resources[resour]
                    last_seen_event = i

        # Codigo para chequear si el final del evento en creacion, pertenece
        # al intervalo de un evento que empieza posteriormente
        for i in range(start=last_seen_event + 1, stop=len(self.events)):
            if i == len(self.events):
                break
            if self.events[i].beginning > end:
                break
            if self.events[i].beginning <= end <= self.events[i].end:
                if resour in self.events[i].needed_resources:
                    resour.in_use += self.events[i].needed_resources[resour]
        ####################################################################

        resour.set_available()
        if resour.available == 0:
            print(f"No hay disponibilidad de {resour.name} en estas fechas\n")

            resour.in_use = 0
            resour.set_available()
            return False

        if amount == None:  # Para evitar input con las dependencias
            amount = resour.ask_amount()
        else:
            if amount > resour.available:
                print(
                    f"No hay {amount} de {resour.name} disponibles en estas fechas\n"
                    f"Solamente se dispone de {resour.available} {resour.name}"
                )

                resour.in_use = 0
                resour.set_available()
                return False

        for dependencie in resour.dependencies:
            amount = resour.dependencies[dependencie]
            check = self.check_resource(dependencie, beginning, end, amount)
            if check == False:
                print(
                    f"Como los\las {resour.name} dependen de {dependencie.name},\
                    no se puede establecer el evento con los recursos solicitados las fechas especificadas"
                )

                resour.in_use = 0
                resour.set_available()
                return False

        resour.in_use = 0
        resour.set_available()
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
