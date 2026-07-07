from core.events import event
from core.resources import resource
from datetime import timedelta, datetime


class planification:
    def __init__(self):
        self.events = []

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
        for event in self.events:
            # Para comprobar si los intervalos de tiempo se intersectan
            if event.beginning < end and beginning < event.end:
                if resour in event.needed_resources:
                    resour.in_use += event.needed_resources[resour]

        resour.set_available()
        available = resour.available

        resour.in_use = 0
        resour.set_available()

        return available

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
