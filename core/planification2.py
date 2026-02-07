from events import event
from resources import resource, list_inventory
from datetime import datetime, timedelta


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

    def check_resource(
        self, resour: resource, beginning: datetime, end: datetime, amount=None
    ):
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

        # Código para chequear si el final del evento en creacion, pertenece
        # al intervalo de un evento que empieza posteriormente
        for i in range(last_seen_event + 1, len(self.events)):
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
                    f"Como l@s {resour.name} dependen de {dependencie.name}\
                    no se puede establecer el evento con los recursos solicitados las fechas especificadas"
                )

                resour.in_use = 0
                resour.set_available()
                return False

        resour.in_use = 0
        resour.set_available()
        return amount

    def find_space(resource):
        pass


# Relacionado con las fechas a la hora de establecer un evento
def valid_datetime(posible_datetime_str):
    formats = [
        "%d/%m/%Y %H:%M",
        "%d-%m-%Y %H:%M",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d-%m-%Y %H:%M:%S",
    ]

    for format in formats:
        try:
            return datetime.strptime(posible_datetime_str, format)
        except ValueError:
            continue
    return False


def confirm_beginning(event_type: str):
    datetime_str = input(
        f"Fecha y hora de inicio de la {event_type} (formato: DD/MM/AAAA HH:MM): "
    )
    datetime_obj = valid_datetime(datetime_str)

    if not datetime_obj:
        print(
            "El formato de la fecha/hora no es válido\n"
            "Pruebe con: DD/MM/AAAA HH:MM, DD-MM-AAAA HH:MM, etc."
        )
        return confirm_beginning(event_type)

    if datetime_obj < datetime.now().replace(second=0, microsecond=0):
        print(
            "Error: Debe establecerse el inicio del evento para ahora, o para algún momento posterior"
        )
        return confirm_beginning(event_type)

    return datetime_obj


def confirm_end(beginning: datetime, event_type: str):
    datetime_str = input(
        f"Fecha y hora de terminación de la {event_type} (formato: DD/MM/AAAA HH:MM): "
    )
    datetime_obj = valid_datetime(datetime_str)

    if not datetime_obj:
        print(
            "El formato de la fecha/hora no es válido\n"
            "Pruebe con: DD/MM/AAAA HH:MM, DD-MM-AAAA HH:MM, etc."
        )
        return confirm_end(beginning, event_type)

    if datetime_obj < beginning:
        print("Error: El evento debe terminar en algún momento posterior a su comienzo")
        return confirm_end(beginning, event_type)

    return datetime_obj


##############################################################
