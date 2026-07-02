from core.events import event
from core.resources import resource
from datetime import timedelta, datetime


class planification:
    def __init__(self):
        self.events = []

    """ Consola en mente
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
    """

    # Adaptacion mas general para enlazar con streamlit
    def valid_event(
        self,
        event_type: str,
        start: datetime,
        end: datetime,
        needed_resources: dict[resource:int],
        description=None,
    ):
        if needed_resources == {}:
            return "Debe asignar al evento al menos un recurso"

        # Definir que todo evento requiere de un salon al menos
        # if salon not in needed_resources:
        #     needed_resources[salon] = 1

        for item, amount in needed_resources.items():
            # Chequear que no haya conflicts
            for r in item.conflicts:
                if r in needed_resources:
                    return f"No se pueden emplear {item.name} cuando están utilizándose en el evento\
                            {r.name}"

            # Chequear disponibilidad
            available = self.resource_availability(item, start, end)

            if available == 0:
                return f"No hay disponibilidad de {item.name} en estas fechas"

            if available < amount:
                return f"Introdujo una cantidad que supera la cantidad disponible de {item.name}"

            for dependencie, amount in item.dependencies.items():
                available2 = self.resource_availability(dependencie, start, end)

                if available2 == 0:
                    return f"No hay disponibilidad de {dependencie.name} en estas fechas,\
                            recurso necesario para disponer de {item.name} "
                if available2 < amount:
                    return f"No hay cantidad suficiente de {dependencie.name} en estas fechas,\
                            recurso necesario para disponer de {item.name} "

        # Despues de tener todo ok
        return event(event_type, start, end, needed_resources, description)

    ########################################################

    def remove_event(self, index):
        if 0 <= index < len(self.events):
            self.events.pop(index)
            return True

        return False

    def resource_availability(
        self, resour: resource, beginning: datetime, end: datetime
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

        # Código para chequear si el final del evento en creación, pertenece
        # al intervalo de un evento que empieza posteriormente
        for i in range(last_seen_event + 1, len(self.events)):
            if self.events[i].beginning > end:
                break
            if self.events[i].beginning <= end <= self.events[i].end:
                if resour in self.events[i].needed_resources:
                    resour.in_use += self.events[i].needed_resources[resour]
        ####################################################################

        resour.set_available()
        available = resour.available

        resour.in_use = 0
        resour.set_available()

        return available

        """ Consola en mente
        if resour.available == 0:
            return f"No hay disponibilidad de {resour.name} en estas fechas\n"

            resour.in_use = 0
            resour.set_available()
            return False

        # Para evitar input con las dependencias
        # if amount == None:
        # amount = resour.ask_amount()
        else:
            if amount > resour.available:
                print(
                    f"No hay {amount} de {resour.name} disponibles en estas fechas\n"
                    f"Solamente se dispone de {resour.available} {resour.name}"
                )

                resour.in_use = 0
                resour.set_available()
                return False

            if amount <= 0:
                return False

        for dependencie in resour.dependencies:
            amount = resour.dependencies[dependencie]
            check = self.check_resource(dependencie, beginning, end, amount)
            if check == False:
                print(
                    f"Como l@s {resour.name} dependen de {dependencie.name}\
                    no se puede establecer el evento con los recursos solicitados en las fechas especificadas"
                )

                resour.in_use = 0
                resour.set_available()
                return False

        resour.in_use = 0
        resour.set_available()
        return amount
        """

    # ***************************************************************************
    def find_space(self, needed_resources, first_search_date, event_duration):
        suggested_beginning = first_search_date
        final_search_date = suggested_beginning + timedelta(days=45)

        while suggested_beginning <= final_search_date:
            suggested_end = suggested_beginning + timedelta(hours=event_duration)
            all_resources_available = True

            # Encontrar el posible día de inicio
            for item, amount in needed_resources.items():
                availability = self.resource_availability(
                    item, suggested_beginning, suggested_end
                )
                if availability < amount:
                    all_resources_available = False
                    break

            if all_resources_available:
                return suggested_beginning, suggested_end
            else:
                suggested_beginning += timedelta(hours=1)

        # Si no hay hueco en los próximos 45 días:
        return None

    # ***************************************************************************


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


""" Consola en mente
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
"""

##############################################################
