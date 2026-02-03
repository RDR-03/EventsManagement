class resource:
    def __init__(self, name, total_cuantity=1, available=0, in_use=0, dependencies={}):
        self.name = name
        self.total_cuantity = total_cuantity
        self.available = available
        self.in_use = in_use
        self.dependencies = dependencies

    def add_resource(self, amount):
        self.total_cuantity += amount
        self.set_available()
        print(f"Se han incorporado {amount} {self.name}")

    def remove_resource(self, amount):
        if amount > self.total_cuantity:
            print(
                f"La cantidad de {self.name} que se desea retirar supera la cantidad total"
            )
        else:
            self.total_cuantity -= amount
            self.set_available()
            print(f"Se han quitado {amount} {self.name}")

    def dependant_on(self, other_resource, amount=1):
        if other_resource.name in self.dependencies:
            return f"Ya está establecida una relación entre {self.name} y {other_resource.name}"

        self.dependencies[other_resource.name] = amount

    def set_available(self):
        self.available = self.total_cuantity - self.in_use

    # Estos son los metodos encargados para la persistencia de datos de la clase con Json
    def to_dict(self):
        return {
            "name": self.name,
            "total_cuantity": self.total_cuantity,
            "available": self.available,
            "in_use": self.in_use,
            "dependencies": self.dependencies,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["total_cuantity"],
            data["available"],
            data["in_use"],
            data["dependencies"],
        )

    ####################################################################################

    def __str__(self):
        return f"{self.name}, Cantidad ({self.total_cuantity})"


def make_inventory(r1: resource, *ri: resource):
    inventory = {}
    inventory[r1.name] = {
        "Total": r1.total_cuantity,
        "Disponibilidad": r1.available,
        "En uso": r1.in_use,
    }
    for r in ri:
        inventory[r.name] = {
            "Total": r.total_cuantity,
            "Disponibilidad": r.available,
            "En uso": r.in_use,
        }

    return inventory


def list_inventory(inventory):
    index = 1
    for item, values in inventory.items():
        print(f"{index} - {item}: {values}")
        index += 1
