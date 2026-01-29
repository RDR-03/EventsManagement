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

    def dependable(self, other_resource, amount=1):
        if other_resource.name in self.dependencies:
            return f"Ya está establecida una relación entre {self.name} y {other_resource.name}"

        self.dependencies[other_resource.name] = amount

    def set_available(self):
        self.available = self.total_cuantity - self.in_use

    # Estos son los metodos encargados de la persistencia de datos con Json
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


r1 = resource("gatos", 5)
r1.add_resource(24)

r2 = resource("raton", 3)
r3 = resource("perro")

r1.dependable(r2)
r1.dependable(r3)

data = r1.to_dict()
recurso = resource.from_dict(data)


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


def list_inventory(i):
    for item, values in i.items():
        print(f"{item}: {values}")
